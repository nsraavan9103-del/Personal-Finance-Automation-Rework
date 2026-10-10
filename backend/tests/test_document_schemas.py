from app.schemas.document import DocumentRead
from datetime import datetime


def test_document_read_schema():
    schema = DocumentRead(
        id=1,
        filename="test.csv",
        file_hash="abc123",
        file_size=1024,
        upload_date=datetime(2024, 1, 1, 0, 0, 0),
        transaction_count=10
    )
    assert schema.filename == "test.csv"
    assert schema.transaction_count == 10
    assert schema.id == 1