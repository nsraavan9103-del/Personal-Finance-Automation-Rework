from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, ForeignKey, func, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    details = Column(String(500), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default='AED', nullable=False)
    debit_credit = Column(String(10), nullable=False, index=True)  # 'Debit' or 'Credit'
    status = Column(String(20), default='SETTLED', nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id', ondelete='CASCADE'), nullable=True, index=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship('Category', backref='transactions')

    __table_args__ = (
        Index('idx_transactions_debit_credit', 'debit_credit'),
        Index('idx_transactions_category', 'category_id'),
    )