import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from io import BytesIO
from app.main import app
from app.core.database import AsyncSessionLocal
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
    await db_session.execute(text("TRUNCATE TABLE transactions, keywords, categories, documents RESTART IDENTITY CASCADE"))
    await db_session.commit()
    
    yield db_session
    
    # Clean up after
    await db_session.execute(text("TRUNCATE TABLE transactions, keywords, categories, documents RESTART IDENTITY CASCADE"))
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


@pytest.mark.asyncio
async def test_upload_creates_document(async_client, db_session):
    csv_content = b"Date,Details,Amount,Debit/Credit\n2024-01-15,TEST MERCHANT,100.00,Debit"
    files = {"file": ("test.csv", BytesIO(csv_content), "text/csv")}
    
    response = await async_client.post("/api/v1/upload/csv", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "document" in data
    assert data["document"]["filename"] == "test.csv"
    assert "file_hash" in data["document"]
    assert data["document"]["transaction_count"] == 1
    assert data["document"]["file_size"] == len(csv_content)