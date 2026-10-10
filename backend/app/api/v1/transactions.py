from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import date
from decimal import Decimal

from app.api.deps import get_db
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import TransactionRead, TransactionSummary

router = APIRouter()


@router.get('', response_model=List[TransactionRead])
async def list_transactions(
    debit_credit: Optional[str] = Query(None, description='Filter by Debit or Credit'),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    limit: int = Query(100, le=1000),
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
    # Get category totals for debits only
    query = (
        select(Category.name, func.sum(Transaction.amount).label('total_amount'))
        .join(Transaction, Transaction.category_id == Category.id)
        .where(Transaction.debit_credit == 'Debit')
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
    )
    result = await db.execute(query)
    return [{'category': row[0], 'total_amount': row[1]} for row in result.all()]


import re

# Corporate suffixes and common variations to normalize
CORPORATE_SUFFIXES = {
    'ltd', 'ltd.', 'limited', 'inc', 'inc.', 'incorporated',
    'corp', 'corp.', 'corporation', 'co', 'co.', 'company',
    'llc', 'llp', 'plc', 'plc.', 'pvt', 'pvt.', 'private',
    'gmbh', 'ag', 'sa', 'nv', 'bv', 'pty', 'pty.', 'proprietary',
    'group', 'holding', 'holdings', 'intl', 'international',
    'global', 'worldwide', 'world', 'international',
    'services', 'service', 'solutions', 'solution',
    'technologies', 'technology', 'tech', 'systems', 'system',
    'industries', 'industry', 'manufacturing', 'mfg',
    'trading', 'trade', 'commerce', 'commercial',
    'enterprises', 'enterprise', 'ventures', 'venture',
    'partners', 'partner', 'associates', 'associate',
    'consulting', 'consultancy', 'advisory', 'advisors',
}

def extract_keyword(details: str) -> str:
    """Extract a clean canonical keyword from transaction details.
    
    Normalizes by:
    - Removing numbers and special characters
    - Removing corporate suffixes (LTD, INC, CORP, etc.)
    - Removing common stop words
    - Keeping first 3 meaningful words in uppercase
    """
    import re
    # Remove numbers and special characters, keep only letters and spaces
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', details)
    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Split into words
    words = cleaned.split()
    # Filter out corporate suffixes and stop words
    stop_words = {
        'the', 'and', 'or', 'for', 'to', 'at', 'in', 'on', 'of', 'a', 'an',
        'ltd', 'ltd.', 'limited', 'inc', 'inc.', 'incorporated',
        'corp', 'corp.', 'corporation', 'co', 'co.', 'company',
        'llc', 'llp', 'plc', 'pvt', 'private', 'group', 'holdings',
    }
    meaningful_words = [w for w in words if len(w) > 2 and w.lower() not in {
        'the', 'and', 'or', 'for', 'to', 'at', 'in', 'on', 'of', 'a', 'an',
        'ltd', 'ltd.', 'limited', 'inc', 'inc.', 'incorporated',
        'corp', 'corp.', 'corporation', 'co', 'co.', 'company',
        'llc', 'llp', 'plc', 'pvt', 'private', 'group', 'holdings',
    }]
    # Take first 3 meaningful words
    keyword = ' '.join(meaningful_words[:3])
    return keyword.upper()


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
    
    # Learn the keyword (add to category keywords if not exists)
    from app.models.keyword import Keyword
    from sqlalchemy import select as sa_select
    from sqlalchemy.exc import IntegrityError
    
    # Extract clean keyword from transaction details
    clean_keyword = extract_keyword(transaction.details)
    
    existing_kw = await db.execute(
        sa_select(Keyword).where(
            Keyword.category_id == category_id,
            func.lower(Keyword.keyword) == clean_keyword.lower()
        )
    )
    if not existing_kw.scalar_one_or_none():
        kw = Keyword(category_id=category_id, keyword=clean_keyword)
        db.add(kw)
        try:
            await db.flush()
        except IntegrityError:
            # Keyword was added by another request - rollback and continue
            await db.rollback()
            # Re-fetch the transaction to ensure it's still valid
            transaction = await db.get(Transaction, transaction_id)
    
    await db.commit()
    await db.refresh(transaction)
    return transaction
