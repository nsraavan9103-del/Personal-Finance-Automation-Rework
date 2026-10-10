from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.api.deps import get_db
from app.models.document import Document
from app.schemas.document import DocumentRead

router = APIRouter()


@router.get('', response_model=List[DocumentRead])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document).order_by(Document.upload_date.desc())
    )
    return result.scalars().all()


@router.delete('/{document_id}', status_code=204)
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db)):
    document = await db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # CASCADE delete handles transactions automatically via FK
    await db.delete(document)
    await db.commit()