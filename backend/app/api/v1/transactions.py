import re
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import date

from app.api.deps import get_db
from app.models.category import Category
from app.models.keyword import Keyword
from app.models.transaction import Transaction
from app.services.categorizer import keyword_match
from app.services.summary import get_expense_summary as get_expense_summary_data
from app.schemas.category import TransactionRead, TransactionSummary

router = APIRouter()


@router.get('', response_model=List[TransactionRead])
async def list_transactions(
    debit_credit: Optional[str] = Query(None, description='Filter by Debit or Credit'),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    limit: int = Query(1000, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    query = select(Transaction).options(selectinload(Transaction.category)).order_by(Transaction.date.desc())

    if debit_credit:
        query = query.where(Transaction.debit_credit == debit_credit)
    if date_from:
        query = query.where(Transaction.date >= date_from)
    if date_to:
        query = query.where(Transaction.date <= date_to)

    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


@router.get('/summary', response_model=List[TransactionSummary])
async def get_expense_summary(db: AsyncSession = Depends(get_db)):
    return await get_expense_summary_data(db)


STOP_WORDS = {
    'the', 'and', 'or', 'for', 'to', 'at', 'in', 'on', 'of', 'a', 'an',
    'ltd', 'ltd.', 'limited', 'inc', 'inc.', 'incorporated',
    'corp', 'corp.', 'corporation', 'co', 'co.', 'company',
    'llc', 'llp', 'plc', 'pvt', 'private', 'group', 'holdings',
}


def extract_keyword(details: str) -> str:
    """Extract a clean canonical keyword from transaction details.

    Removes numbers/special characters and stop words, keeps first 3 meaningful words.
    """
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', details)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    meaningful_words = [w for w in cleaned.split() if len(w) > 2 and w.lower() not in STOP_WORDS]
    return ' '.join(meaningful_words[:3]).upper()


@router.put('/{transaction_id}/category', response_model=TransactionRead)
async def update_transaction_category(
    transaction_id: int,
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    transaction = await db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction not found')

    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')

    # Update transaction category (manual categorization - should be preserved)
    transaction.category_id = category_id
    # Keep the relationship loaded in memory for the response — refresh/lazy-load
    # outside greenlet context raises MissingGreenlet (500).
    transaction.category = category
    # Flush before the savepoint so a keyword race can't roll the category change back
    await db.flush()

    # Learn the keyword (add to category keywords if not exists)
    clean_keyword = extract_keyword(transaction.details)

    existing_kw = await db.execute(
        select(Keyword).where(
            Keyword.category_id == category_id,
            func.lower(Keyword.keyword) == clean_keyword.lower()
        )
    )
    if not existing_kw.scalar_one_or_none():
        kw = Keyword(category_id=category_id, keyword=clean_keyword)
        # Savepoint: a duplicate-keyword race must not roll back the category change
        async with db.begin_nested():
            db.add(kw)

    # Auto-categorize: all transactions whose details match any keyword of this
    # category move to it. Unique detail values only, compared case-insensitively.
    kw_rows = await db.execute(select(Keyword.keyword).where(Keyword.category_id == category_id))
    category_keywords = [k.lower() for k in kw_rows.scalars().all()]
    detail_rows = await db.execute(select(Transaction.details).distinct())
    matched_details = [
        d for d in detail_rows.scalars().all()
        if any(keyword_match(k, d.lower()) for k in category_keywords)
    ]
    if matched_details:
        await db.execute(
            update(Transaction)
            .where(Transaction.details.in_(matched_details))
            .values(category_id=category_id)
        )

    await db.commit()
    return transaction
