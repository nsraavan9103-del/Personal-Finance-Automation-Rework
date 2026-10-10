import pytest
from app.models.document import Document
from app.models.transaction import Transaction
from sqlalchemy import inspect


def test_document_model_exists():
    assert hasattr(Document, '__tablename__')
    assert Document.__tablename__ == 'documents'


def test_document_columns():
    cols = {c.name for c in Document.__table__.columns}
    expected = {'id', 'filename', 'file_hash', 'file_size', 'upload_date', 'transaction_count'}
    assert expected.issubset(cols)


def test_transaction_has_document_fk():
    txn_cols = {c.name for c in Transaction.__table__.columns}
    assert 'document_id' in txn_cols
    fk = [fk for fk in Transaction.__table__.foreign_keys if fk.column.table.name == 'documents']
    assert len(fk) == 1
    assert fk[0].ondelete == 'CASCADE'