from pydantic import BaseModel
from typing import List
from decimal import Decimal
from app.schemas.category import CategoryRead, TransactionRead, TransactionSummary
from app.schemas.document import DocumentRead


class UploadResponse(BaseModel):
    message: str
    transactions_created: int
    categories: List[CategoryRead]
    summary: List[TransactionSummary]
    document: DocumentRead