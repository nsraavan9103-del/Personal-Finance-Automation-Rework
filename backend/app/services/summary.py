from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict, Any

from app.models.category import Category
from app.models.transaction import Transaction


async def get_expense_summary(db: AsyncSession) -> List[Dict[str, Any]]:
    """Get category totals for debits only."""
    query = (
        select(Category.name, func.sum(Transaction.amount).label('total_amount'))
        .join(Transaction, Transaction.category_id == Category.id)
        .where(Transaction.debit_credit == 'Debit')
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
    )
    result = await db.execute(query)
    return [{'category': row[0], 'total_amount': row[1]} for row in result.all()]