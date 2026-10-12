import pytest
from httpx import AsyncClient
from io import BytesIO
from app.main import app


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