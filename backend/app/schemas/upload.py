from pydantic import BaseModel
from typing import List
from app.schemas.category import CategoryRead, TransactionRead
from app.schemas.document import DocumentRead


class UploadResponse(BaseModel):
    message: str
    transactions_created: int
    categories: List[CategoryRead]
    document: DocumentRead