from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentRead(BaseModel):
    id: int
    filename: str
    file_hash: str
    file_size: int
    upload_date: datetime
    transaction_count: int

    class Config:
        from_attributes = True