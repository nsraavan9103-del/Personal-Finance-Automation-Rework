from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False, index=True)
    keyword = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship('Category', back_populates='keywords')

    __table_args__ = (UniqueConstraint('category_id', 'keyword', name='uq_category_keyword'),)
