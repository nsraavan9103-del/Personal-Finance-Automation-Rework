from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_hash = Column(String(64), nullable=False, index=True)
    file_size = Column(Integer, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    transaction_count = Column(Integer, default=0)