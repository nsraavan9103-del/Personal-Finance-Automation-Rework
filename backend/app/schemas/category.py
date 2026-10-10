from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class KeywordBase(BaseModel):
    keyword: str


class KeywordCreate(KeywordBase):
    pass


class KeywordRead(KeywordBase):
    id: int
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    date: date
    details: str
    amount: Decimal
    currency: str = 'AED'
    debit_credit: str
    status: str = 'SETTLED'
    category_id: Optional[int] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int
    uploaded_at: datetime
    category: Optional[CategoryRead] = None

    class Config:
        from_attributes = True


class TransactionSummary(BaseModel):
    category: str
    total_amount: Decimal
