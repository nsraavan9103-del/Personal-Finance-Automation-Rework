import pytest
from decimal import Decimal
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.services.summary import get_expense_summary
from app.core.database import AsyncSessionLocal
from app.models.category import Category
from app.models.transaction import Transaction


@pytest.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def clean_db(db_session: AsyncSession):
    """Clean up database before and after each test."""
    # Clean up before - use TRUNCATE for faster cleanup with CASCADE
    await db_session.execute(text("TRUNCATE TABLE transactions, keywords, categories RESTART IDENTITY CASCADE"))
    await db_session.commit()
    
    yield db_session
    
    # Clean up after
    await db_session.execute(text("TRUNCATE TABLE transactions, keywords, categories RESTART IDENTITY CASCADE"))
    await db_session.commit()


class TestSummaryService:
    """Tests for the summary service."""

    @pytest.mark.asyncio
    async def test_get_expense_summary_empty(self, clean_db):
        """Test summary with no transactions."""
        summary = await get_expense_summary(clean_db)
        assert summary == []

    @pytest.mark.asyncio
    async def test_get_expense_summary_single_category(self, clean_db):
        """Test summary with single category."""
        cat = Category(name='Food')
        clean_db.add(cat)
        await clean_db.flush()
        
        t1 = Transaction(
            date=date(2024, 1, 15), details='STARBUCKS', amount=Decimal('25.50'),
            currency='AED', debit_credit='Debit', category_id=cat.id
        )
        clean_db.add(t1)
        await clean_db.commit()
        
        summary = await get_expense_summary(clean_db)
        
        assert len(summary) == 1
        assert summary[0]['category'] == 'Food'
        assert summary[0]['total_amount'] == Decimal('25.50')

    @pytest.mark.asyncio
    async def test_get_expense_summary_multiple_categories(self, clean_db):
        """Test summary with multiple categories."""
        food_cat = Category(name='Food')
        transport_cat = Category(name='Transport')
        clean_db.add_all([food_cat, transport_cat])
        await clean_db.flush()
        
        transactions = [
            Transaction(date=date(2024, 1, 15), details='STARBUCKS', amount=Decimal('25.50'), currency='AED', debit_credit='Debit', category_id=food_cat.id),
            Transaction(date=date(2024, 1, 16), details='UBER', amount=Decimal('45.00'), currency='AED', debit_credit='Debit', category_id=transport_cat.id),
            Transaction(date=date(2024, 1, 17), details='LUNCH', amount=Decimal('30.00'), currency='AED', debit_credit='Debit', category_id=food_cat.id),
        ]
        clean_db.add_all(transactions)
        await clean_db.commit()
        
        summary = await get_expense_summary(clean_db)
        
        assert len(summary) == 2
        # Should be sorted by total amount descending
        assert summary[0]['category'] == 'Food'
        assert summary[0]['total_amount'] == Decimal('55.50')
        assert summary[1]['category'] == 'Transport'
        assert summary[1]['total_amount'] == Decimal('45.00')

    @pytest.mark.asyncio
    async def test_get_expense_summary_excludes_credits(self, clean_db):
        """Test that summary only includes debits, not credits."""
        cat = Category(name='Food')
        clean_db.add(cat)
        await clean_db.flush()
        
        # Add both debit and credit transactions
        debit_txn = Transaction(date=date(2024, 1, 15), details='STARBUCKS', amount=Decimal('25.50'), currency='AED', debit_credit='Debit', category_id=cat.id)
        credit_txn = Transaction(date=date(2024, 1, 16), details='REFUND', amount=Decimal('100.00'), currency='AED', debit_credit='Credit', category_id=cat.id)
        clean_db.add_all([debit_txn, credit_txn])
        await clean_db.commit()
        
        summary = await get_expense_summary(clean_db)
        
        assert len(summary) == 1
        assert summary[0]['total_amount'] == Decimal('25.50')  # Only debit counted

    @pytest.mark.asyncio
    async def test_get_expense_summary_excludes_uncategorized(self, clean_db):
        """Test that summary excludes transactions with no category (null category_id)."""
        cat = Category(name='Food')
        clean_db.add(cat)
        await clean_db.flush()
        
        # Transaction with category
        cat_txn = Transaction(date=date(2024, 1, 15), details='STARBUCKS', amount=Decimal('25.50'), currency='AED', debit_credit='Debit', category_id=cat.id)
        # Transaction without category
        uncategorized_txn = Transaction(date=date(2024, 1, 16), details='UNKNOWN', amount=Decimal('50.00'), currency='AED', debit_credit='Debit', category_id=None)
        clean_db.add_all([cat_txn, uncategorized_txn])
        await clean_db.commit()
        
        summary = await get_expense_summary(clean_db)
        
        assert len(summary) == 1
        assert summary[0]['category'] == 'Food'
        assert summary[0]['total_amount'] == Decimal('25.50')

    @pytest.mark.asyncio
    async def test_get_expense_summary_sorts_by_amount_desc(self, clean_db):
        """Test that summary is sorted by total amount descending."""
        cat1 = Category(name='Low Spend')
        cat2 = Category(name='Medium Spend')
        cat3 = Category(name='High Spend')
        clean_db.add_all([cat1, cat2, cat3])
        await clean_db.flush()
        
        transactions = [
            Transaction(date=date(2024, 1, 15), details='LOW', amount=Decimal('10.00'), currency='AED', debit_credit='Debit', category_id=cat1.id),
            Transaction(date=date(2024, 1, 16), details='MEDIUM', amount=Decimal('100.00'), currency='AED', debit_credit='Debit', category_id=cat2.id),
            Transaction(date=date(2024, 1, 17), details='HIGH', amount=Decimal('500.00'), currency='AED', debit_credit='Debit', category_id=cat3.id),
        ]
        clean_db.add_all(transactions)
        await clean_db.commit()
        
        summary = await get_expense_summary(clean_db)
        
        assert len(summary) == 3
        assert summary[0]['category'] == 'High Spend'
        assert summary[0]['total_amount'] == Decimal('500.00')
        assert summary[1]['category'] == 'Medium Spend'
        assert summary[1]['total_amount'] == Decimal('100.00')
        assert summary[2]['category'] == 'Low Spend'
        assert summary[2]['total_amount'] == Decimal('10.00')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])