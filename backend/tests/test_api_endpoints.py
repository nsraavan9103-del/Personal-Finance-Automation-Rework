import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, delete
from datetime import date
from app.main import app
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.category import Category
from app.models.keyword import Keyword
from app.models.transaction import Transaction
from app.api.deps import get_db


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


@pytest.fixture(scope="function")
async def async_client(clean_db: AsyncSession):
    """Create an async HTTP client for testing with database session override."""
    # Override the get_db dependency to use our test session
    async def override_get_db():
        yield clean_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Clean up override
    app.dependency_overrides.clear()


class TestCategoriesAPI:
    """Tests for Categories API endpoints."""

    @pytest.mark.asyncio
    async def test_list_categories_empty(self, async_client: AsyncClient, clean_db):
        """Test listing categories when empty."""
        response = await async_client.get("/api/v1/categories")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_create_category(self, async_client: AsyncClient, clean_db):
        """Test creating a new category."""
        response = await async_client.post("/api/v1/categories", json={"name": "Food"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Food"
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_duplicate_category(self, async_client: AsyncClient, clean_db):
        """Test creating duplicate category fails."""
        await async_client.post("/api/v1/categories", json={"name": "Food"})
        response = await async_client.post("/api/v1/categories", json={"name": "Food"})
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_list_categories(self, async_client: AsyncClient, clean_db):
        """Test listing all categories."""
        await async_client.post("/api/v1/categories", json={"name": "Food"})
        await async_client.post("/api/v1/categories", json={"name": "Transport"})
        
        response = await async_client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        names = {c["name"] for c in data}
        assert "Food" in names
        assert "Transport" in names

    @pytest.mark.asyncio
    async def test_delete_category(self, async_client: AsyncClient, clean_db):
        """Test deleting a category."""
        response = await async_client.post("/api/v1/categories", json={"name": "Food"})
        category_id = response.json()["id"]
        
        response = await async_client.delete(f"/api/v1/categories/{category_id}")
        assert response.status_code == 204
        
        # Verify deleted
        response = await async_client.get("/api/v1/categories")
        assert len(response.json()) == 0

    @pytest.mark.asyncio
    async def test_delete_uncategorized_protected(self, async_client: AsyncClient, clean_db):
        """Test that Uncategorized category cannot be deleted."""
        # First ensure Uncategorized exists using the test session
        from app.models.category import Category
        from sqlalchemy import select
        
        result = await clean_db.execute(select(Category).where(Category.name == "Uncategorized"))
        uncategorized = result.scalar_one_or_none()
        if not uncategorized:
            uncategorized = Category(name="Uncategorized")
            clean_db.add(uncategorized)
            await clean_db.flush()
            await clean_db.commit()
        
        uncategorized_id = uncategorized.id
        
        response = await async_client.delete(f"/api/v1/categories/{uncategorized_id}")
        assert response.status_code == 400
        assert "cannot delete" in response.json()["detail"].lower()


class TestCategoriesKeywordsAPI:
    """Tests for Category Keywords API endpoints."""

    @pytest.mark.asyncio
    async def test_list_keywords(self, async_client: AsyncClient, clean_db):
        """Test listing keywords for a category."""
        # Create category and keyword using test session
        from app.models.category import Category
        from app.models.keyword import Keyword
        cat = Category(name="Food")
        clean_db.add(cat)
        await clean_db.flush()
        kw = Keyword(category_id=cat.id, keyword="STARBUCKS")
        clean_db.add(kw)
        await clean_db.commit()
        cat_id = cat.id
        
        response = await async_client.get(f"/api/v1/categories/{cat_id}/keywords")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["keyword"] == "STARBUCKS"

    @pytest.mark.asyncio
    async def test_add_keyword(self, async_client: AsyncClient, clean_db):
        """Test adding a keyword to a category."""
        response = await async_client.post("/api/v1/categories", json={"name": "Food"})
        cat_id = response.json()["id"]
        
        response = await async_client.post(f"/api/v1/categories/{cat_id}/keywords", json={"keyword": "STARBUCKS"})
        assert response.status_code == 201
        data = response.json()
        assert data["keyword"] == "STARBUCKS"
        assert data["category_id"] == cat_id

    @pytest.mark.asyncio
    async def test_add_duplicate_keyword(self, async_client: AsyncClient, clean_db):
        """Test adding duplicate keyword fails."""
        response = await async_client.post("/api/v1/categories", json={"name": "Food"})
        cat_id = response.json()["id"]
        
        await async_client.post(f"/api/v1/categories/{cat_id}/keywords", json={"keyword": "STARBUCKS"})
        response = await async_client.post(f"/api/v1/categories/{cat_id}/keywords", json={"keyword": "STARBUCKS"})
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()


class TestTransactionsAPI:
    """Tests for Transactions API endpoints."""

    @pytest.mark.asyncio
    async def test_list_transactions_empty(self, async_client: AsyncClient, clean_db):
        """Test listing transactions when empty."""
        response = await async_client.get("/api/v1/transactions")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_list_transactions_with_filters(self, async_client: AsyncClient, clean_db):
        """Test listing transactions with filters."""
        cat = Category(name="Food")
        clean_db.add(cat)
        await clean_db.flush()
        
        txns = [
            Transaction(date=date(2024, 1, 15), details='STARBUCKS', amount=25.50, currency='AED', debit_credit='Debit', category_id=cat.id),
            Transaction(date=date(2024, 1, 16), details='SALARY', amount=5000.00, currency='AED', debit_credit='Credit', category_id=None),
        ]
        clean_db.add_all(txns)
        await clean_db.commit()
        
        # Filter by debit
        response = await async_client.get("/api/v1/transactions?debit_credit=Debit")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["debit_credit"] == "Debit"
        
        # Filter by credit
        response = await async_client.get("/api/v1/transactions?debit_credit=Credit")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["debit_credit"] == "Credit"

    @pytest.mark.asyncio
    async def test_get_expense_summary(self, async_client: AsyncClient, clean_db):
        """Test getting expense summary."""
        cat = Category(name="Food")
        clean_db.add(cat)
        await clean_db.flush()
        
        txns = [
            Transaction(date=date(2024, 1, 15), details='STARBUCKS', amount=25.50, currency='AED', debit_credit='Debit', category_id=cat.id),
            Transaction(date=date(2024, 1, 16), details='SALARY', amount=5000.00, currency='AED', debit_credit='Credit', category_id=None),
        ]
        clean_db.add_all(txns)
        await clean_db.commit()
        
        response = await async_client.get("/api/v1/transactions/summary")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "Food"  # Transaction has category_id set
        assert float(data[0]["total_amount"]) > 0

    @pytest.mark.asyncio
    async def test_update_transaction_category(self, async_client: AsyncClient, clean_db):
        """Test updating transaction category and learning keyword."""
        cat = Category(name="Food")
        clean_db.add(cat)
        await clean_db.flush()
        
        txn = Transaction(date=date(2024, 1, 15), details='STARBUCKS', amount=25.50, currency='AED', debit_credit='Debit', category_id=None)
        clean_db.add(txn)
        await clean_db.commit()
        await clean_db.refresh(txn)
        txn_id = txn.id
        cat_id = cat.id
        
        response = await async_client.put(f"/api/v1/transactions/{txn_id}/category?category_id={cat_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["category_id"] == cat_id
        
        # Verify keyword was learned
        async with AsyncSessionLocal() as db:
            from app.models.keyword import Keyword
            from sqlalchemy import select, func
            result = await db.execute(select(Keyword).where(Keyword.category_id == cat_id, func.lower(Keyword.keyword) == 'starbucks'))
            kw = result.scalar_one_or_none()
            assert kw is not None
            assert kw.keyword == "STARBUCKS"


class TestUploadAPI:
    """Tests for Upload API endpoints."""

    @pytest.mark.asyncio
    async def test_upload_csv_success(self, async_client: AsyncClient, clean_db):
        """Test successful CSV upload."""
        # Ensure Uncategorized category exists
        from app.models.category import Category
        uncategorized = Category(name="Uncategorized")
        clean_db.add(uncategorized)
        await clean_db.commit()
        
        csv_content = b"Date,Details,Amount,Debit/Credit\n15 Jan 2024,STARBUCKS,25.50,Debit\n16 Jan 2024,SALARY,5000.00,Credit"
        
        files = {"file": ("test.csv", csv_content, "text/csv")}
        response = await async_client.post("/api/v1/upload/csv", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["transactions_created"] == 2
        assert len(data["categories"]) >= 1
        assert len(data["summary"]) >= 0

    @pytest.mark.asyncio
    async def test_upload_non_csv_fails(self, async_client: AsyncClient, clean_db):
        """Test that non-CSV files are rejected."""
        files = {"file": ("test.txt", b"not a csv", "text/plain")}
        response = await async_client.post("/api/v1/upload/csv", files=files)
        assert response.status_code == 400
        assert "csv" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_upload_invalid_csv_fails(self, async_client: AsyncClient, clean_db):
        """Test that invalid CSV format fails."""
        csv_content = b"Invalid,Data\nNo,Headers"
        files = {"file": ("test.csv", csv_content, "text/csv")}
        response = await async_client.post("/api/v1/upload/csv", files=files)
        assert response.status_code == 400
        assert "csv" in response.json()["detail"].lower()


class TestHealthCheck:
    """Tests for health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check(self, async_client: AsyncClient):
        """Test health check endpoint."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


if __name__ == '__main__':
    pytest.main([__file__, '-v'])