from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hashlib

from app.api.deps import get_db
from app.models.category import Category
from app.models.keyword import Keyword
from app.models.transaction import Transaction
from app.models.document import Document
from app.services.csv_parser import parse_csv
from app.services.categorizer import categorize_transactions
from app.schemas.category import CategoryRead
from app.schemas.upload import UploadResponse
from app.schemas.document import DocumentRead

router = APIRouter()


@router.post('/csv', response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail='File must be a CSV')

    content = await file.read()

    # Compute file hash and reject duplicate content
    file_hash = hashlib.sha256(content).hexdigest()
    file_size = len(content)
    dup = await db.execute(select(Document).where(Document.file_hash == file_hash))
    if dup.scalar_one_or_none():
        raise HTTPException(status_code=409, detail='This file has already been uploaded')

    try:
        df = parse_csv(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'CSV parsing error: {str(e)}')
    
    # Load all categories and keywords for categorization
    categories_result = await db.execute(select(Category))
    categories = categories_result.scalars().all()
    
    keywords_result = await db.execute(select(Keyword))
    keywords = keywords_result.scalars().all()
    
    # Build keyword map: {keyword_lower: category_id}
    keyword_map = {kw.keyword.lower().strip(): kw.category_id for kw in keywords}
    uncategorized_id = next((c.id for c in categories if c.name == 'Uncategorized'), None)
    
    # Categorize transactions
    df = categorize_transactions(df, keyword_map, uncategorized_id)
    
    # Create Document record
    document = Document(
        filename=file.filename,
        file_hash=file_hash,
        file_size=file_size,
        transaction_count=len(df)
    )
    db.add(document)
    await db.flush()  # get document.id
    
    # Save transactions to database with document_id
    transactions = []
    for _, row in df.iterrows():
        category_id = row['Category'] if row['Category'] != 'Uncategorized' else uncategorized_id
        txn = Transaction(
            date=row['Date'].date(),
            details=row['Details'],
            amount=row['Amount'],
            currency=row.get('Currency', 'AED'),
            debit_credit=row['Debit/Credit'],
            status=row.get('Status', 'SETTLED'),
            category_id=category_id,
            document_id=document.id
        )
        db.add(txn)
        transactions.append(txn)
    
    await db.commit()
    await db.refresh(document)

    categories_result = await db.execute(select(Category))
    categories_list = categories_result.scalars().all()

    return UploadResponse(
        message=f'Successfully uploaded {len(transactions)} transactions',
        transactions_created=len(transactions),
        categories=[CategoryRead.model_validate(c) for c in categories_list],
        document=DocumentRead.model_validate(document)
    )