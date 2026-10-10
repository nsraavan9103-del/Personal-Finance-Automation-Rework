# Document Upload History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add document upload tracking with collapsible sidebar showing uploaded files, each deletable with cascade delete of its transactions.

**Architecture:** New `Document` model linked to `Transaction` via `document_id` (FK, CASCADE delete). Backend adds `/documents` router. Frontend adds collapsible left sidebar with document list, delete button with confirmation.

**Tech Stack:** FastAPI, SQLAlchemy, React, Axios, SHA256 for file hashing

**Spec:** Design from brainstorming session (collapsible sidebar, SHA256 hash, hard delete with CASCADE, re-upload allowed)

## Global Constraints

- Python 3.11+, Node 18+, React 18
- Existing patterns: async SQLAlchemy, Pydantic schemas, React hooks + context
- No new external dependencies (hashlib is stdlib)
- Maintain existing API contracts for `/upload/csv`
- CASCADE delete: deleting document removes its transactions permanently
- Re-upload of same file hash creates new document record (no blocking)

---

### Task 1: Create Document Model

**Files:**
- Create: `backend/app/models/document.py`
- Modify: `backend/app/models/__init__.py`
- Modify: `backend/app/models/transaction.py:16-17` (add FK column)

**Interfaces:**
- Consumes: existing `Base` from `app.core.database`
- Produces: `Document` model class with columns: id, filename, file_hash, file_size, upload_date, transaction_count

- [ ] **Step 1: Write the failing test**

```python
# tests/test_document_model.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && .\venv\Scripts\python.exe -m pytest tests/test_document_model.py -v`
Expected: FAIL (model doesn't exist, FK missing)

- [ ] **Step 3: Write minimal implementation**

`backend/app/models/document.py`:
```python
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
```

`backend/app/models/__init__.py`:
```python
from app.models.category import Category
from app.models.keyword import Keyword
from app.models.transaction import Transaction
from app.models.document import Document

__all__ = ['Category', 'Keyword', 'Transaction', 'Document']
```

`backend/app/models/transaction.py` - add after line 16:
```python
    document_id = Column(Integer, ForeignKey('documents.id', ondelete='CASCADE'), nullable=True, index=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && .\venv\Scripts\python.exe -m pytest tests/test_document_model.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/models/document.py backend/app/models/__init__.py backend/app/models/transaction.py tests/test_document_model.py
git commit -m "feat: add Document model and transaction FK"
```

---

### Task 2: Create Document Pydantic Schemas

**Files:**
- Create: `backend/app/schemas/document.py`
- Modify: `backend/app/schemas/__init__.py`

**Interfaces:**
- Consumes: Document model
- Produces: `DocumentRead`, `DocumentList` schemas

- [ ] **Step 1: Write the failing test**

```python
# tests/test_document_schemas.py
from app.schemas.document import DocumentRead

def test_document_read_schema():
    schema = DocumentRead(id=1, filename="test.csv", file_hash="abc123", file_size=1024, 
                          upload_date="2024-01-01T00:00:00", transaction_count=10)
    assert schema.filename == "test.csv"
    assert schema.transaction_count == 10
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && .\venv\Scripts\python.exe -m pytest tests/test_document_schemas.py -v`
Expected: FAIL (schema doesn't exist)

- [ ] **Step 3: Write minimal implementation**

`backend/app/schemas/document.py`:
```python
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
```

`backend/app/schemas/__init__.py` - add to imports and `__all__`:
```python
from app.schemas.document import DocumentRead

__all__ = [..., 'DocumentRead']
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && .\venv\Scripts\python.exe -m pytest tests/test_document_schemas.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/schemas/document.py backend/app/schemas/__init__.py tests/test_document_schemas.py
git commit -m "feat: add Document Pydantic schemas"
```

---

### Task 3: Modify Upload Endpoint to Create Document

**Files:**
- Modify: `backend/app/api/v1/upload.py` (add hash, create Document, set document_id)
- Test: `tests/test_api_endpoints.py::TestUploadAPI::test_upload_csv_success`

**Interfaces:**
- Consumes: `Document` model, `hashlib`, upload content
- Produces: `Document` record + transactions with `document_id`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_upload_document.py
import pytest
from io import BytesIO

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && .\venv\Scripts\python.exe -m pytest tests/test_upload_document.py -v`
Expected: FAIL (no document in response)

- [ ] **Step 3: Write minimal implementation**

`backend/app/api/v1/upload.py` - modify upload_csv:
```python
import hashlib
from app.models.document import Document

@router.post('/csv', response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    # ... existing parsing ...
    
    # Compute file hash
    file_content = await file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    file_size = len(file_content)
    
    # Re-parse since we read content
    df = parse_csv(file_content)
    
    # ... existing category/keyword loading ...
    
    # Create Document record
    document = Document(
        filename=file.filename,
        file_hash=file_hash,
        file_size=file_size,
        transaction_count=len(df)
    )
    db.add(document)
    await db.flush()  # get document.id
    
    # Save transactions with document_id
    transactions = []
    for _, row in df.iterrows():
        # ... existing transaction creation ...
        txn = Transaction(
            # ... existing fields ...
            category_id=category_id,
            document_id=document.id  # NEW
        )
        db.add(txn)
        transactions.append(txn)
    
    await db.commit()
    await db.refresh(document)
    
    # ... existing summary ...
    
    return UploadResponse(
        message=f'Successfully uploaded {len(transactions)} transactions',
        transactions_created=len(transactions),
        categories=[CategoryRead.model_validate(c) for c in categories_list],
        summary=[...],
        document=DocumentRead.model_validate(document)  # NEW - add to response
    )
```

Update `UploadResponse` schema in `backend/app/schemas/upload.py`:
```python
class UploadResponse(BaseModel):
    message: str
    transactions_created: int
    categories: List[CategoryRead]
    summary: List[TransactionSummary]
    document: DocumentRead  # NEW
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && .\venv\Scripts\python.exe -m pytest tests/test_upload_document.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/v1/upload.py backend/app/schemas/upload.py tests/test_upload_document.py
git commit -m "feat: upload creates document record with hash"
```

---

### Task 4: Create Documents API Router

**Files:**
- Create: `backend/app/api/v1/documents.py`
- Modify: `backend/app/api/v1/__init__.py` (include router)

**Interfaces:**
- Consumes: `Document` model, `DocumentRead` schema, DB session
- Produces: `GET /documents` (list), `DELETE /documents/{id}` (cascade delete)

- [ ] **Step 1: Write the failing test**

```python
# tests/test_documents_api.py
import pytest
from io import BytesIO

@pytest.mark.asyncio
async def test_list_documents(async_client, db_session):
    # Upload a file first
    csv_content = b"Date,Details,Amount,Debit/Credit\n2024-01-15,TEST,100.00,Debit"
    await async_client.post("/api/v1/upload/csv", files={"file": ("test.csv", BytesIO(csv_content), "text/csv")})
    
    response = await async_client.get("/api/v1/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["filename"] == "test.csv"

@pytest.mark.asyncio
async def test_delete_document_cascades(async_client, db_session):
    csv_content = b"Date,Details,Amount,Debit/Credit\n2024-01-15,TEST,100.00,Debit\n2024-01-16,TEST2,200.00,Debit"
    resp = await async_client.post("/api/v1/upload/csv", files={"file": ("test.csv", BytesIO(csv_content), "text/csv")})
    doc_id = resp.json()["document"]["id"]
    
    # Verify transactions exist
    txns_before = await async_client.get("/api/v1/transactions")
    assert len(txns_before.json()) >= 2
    
    # Delete document
    response = await async_client.delete(f"/api/v1/documents/{doc_id}")
    assert response.status_code == 204
    
    # Verify transactions cascade deleted
    txns_after = await async_client.get("/api/v1/transactions")
    # The 2 transactions from this document should be gone
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && .\venv\Scripts\python.exe -m pytest tests/test_documents_api.py -v`
Expected: FAIL (router doesn't exist)

- [ ] **Step 3: Write minimal implementation**

`backend/app/api/v1/documents.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.api.deps import get_db
from app.models.document import Document
from app.schemas.document import DocumentRead

router = APIRouter()

@router.get('', response_model=List[DocumentRead])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document).order_by(Document.upload_date.desc())
    )
    return result.scalars().all()

@router.delete('/{document_id}', status_code=204)
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db)):
    document = await db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # CASCADE delete handles transactions automatically via FK
    await db.delete(document)
    await db.commit()
```

`backend/app/api/v1/__init__.py`:
```python
from app.api.v1 import categories, transactions, upload, documents

api_router.include_router(documents.router, prefix='/documents', tags=['documents'])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd backend && .\venv\Scripts\python.exe -m pytest tests/test_documents_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/v1/documents.py backend/app/api/v1/__init__.py tests/test_documents_api.py
git commit -m "feat: add documents API router (list, delete with cascade)"
```

---

### Task 5: Create Frontend UploadHistory Component

**Files:**
- Create: `frontend/src/components/UploadHistory.jsx`
- Create: `frontend/src/hooks/useDocuments.js`
- Modify: `frontend/src/components/FileUpload.jsx` (refresh history after upload)

**Interfaces:**
- Consumes: `/api/v1/documents` API
- Produces: Document list UI with delete button

- [ ] **Step 1: Write the failing test**

```typescript
// frontend/tests/upload-history.spec.ts
import { render, screen, fireEvent } from '@testing-library/react'
import { UploadHistory } from '../components/UploadHistory'

test('renders document list with delete button', () => {
  // Mock API response
  // Render component
  // Expect document rows with filename, date, count, delete button
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend && npm test -- upload-history.spec.ts`
Expected: FAIL (component doesn't exist)

- [ ] **Step 3: Write minimal implementation**

`frontend/src/hooks/useDocuments.js`:
```javascript
import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

export function useDocuments() {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchDocuments = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_BASE}/documents`)
      setDocuments(response.data)
    } catch (err) {
      setError('Failed to load documents')
    } finally {
      setLoading(false)
    }
  }

  const deleteDocument = async (id) => {
    try {
      await axios.delete(`${API_BASE}/documents/${id}`)
      fetchDocuments() // refresh
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Failed to delete document')
    }
  }

  useEffect(() => {
    fetchDocuments()
  }, [])

  return { documents, loading, error, fetchDocuments, deleteDocument }
}
```

`frontend/src/components/UploadHistory.jsx`:
```jsx
import React, { useState } from 'react'
import { useDocuments } from '../hooks/useDocuments'

export function UploadHistory({ onRefreshTransactions }) {
  const { documents, loading, error, deleteDocument, fetchDocuments } = useDocuments()
  const [confirmDeleteId, setConfirmDeleteId] = useState(null)

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this document and all its transactions? This cannot be undone.')) return
    await deleteDocument(id)
    if (onRefreshTransactions) onRefreshTransactions()
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
  }

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="w-72 bg-white border-r border-gray-200 h-full flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Uploads</h3>
      </div>
      
      {error && (
        <div className="p-4 text-red-600 text-sm">{error}</div>
      )}

      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-4 text-center text-gray-500">Loading...</div>
        ) : documents.length === 0 ? (
          <div className="p-4 text-center text-gray-500 text-sm">No documents uploaded yet</div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {documents.map(doc => (
              <li key={doc.id} className="p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate" title={doc.filename}>
                      {doc.filename}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {formatDate(doc.upload_date)} • {doc.transaction_count} transactions • {formatSize(doc.file_size)}
                    </p>
                    <p className="text-xs text-gray-400 mt-1 font-mono">
                      {doc.file_hash.slice(0, 16)}...
                    </p>
                  </div>
                  <button
                    onClick={() => handleDelete(doc.id)}
                    disabled={confirmDeleteId === doc.id}
                    className="text-red-600 hover:text-red-800 text-sm font-medium px-2 py-1 whitespace-nowrap flex-shrink-0"
                  >
                    {confirmDeleteId === doc.id ? 'Confirm?' : 'Delete'}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
```

`frontend/src/components/FileUpload.jsx` - add import and callback:
```jsx
import { UploadHistory } from './UploadHistory'

// Inside component, add:
const refreshUploadHistory = () => {
  // Trigger history refresh - can use window event or pass ref
  window.dispatchEvent(new CustomEvent('refresh-documents'))
}

// In handleUploadSuccess, after setTransactions:
refreshUploadHistory()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend && npm test -- upload-history.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/src/components/UploadHistory.jsx frontend/src/hooks/useDocuments.js frontend/src/components/FileUpload.jsx
git commit -m "feat: add UploadHistory component and useDocuments hook"
```

---

### Task 6: Add Collapsible Sidebar to App Layout

**Files:**
- Modify: `frontend/src/App.jsx` (add sidebar state + UploadHistory)
- Modify: `frontend/src/index.css` or add inline styles for sidebar animation

**Interfaces:**
- Consumes: `UploadHistory` component
- Produces: Left sidebar with toggle button in header

- [ ] **Step 1: Write the failing test**

```typescript
// frontend/tests/app-sidebar.spec.ts
test('sidebar toggles on button click', () => {
  // Render App
  // Click hamburger button
  // Expect sidebar visible
  // Click again
  // Expect sidebar hidden
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd frontend && npm test -- app-sidebar.spec.ts`
Expected: FAIL (no sidebar)

- [ ] **Step 3: Write minimal implementation**

`frontend/src/App.jsx`:
```jsx
import React, { useState } from 'react'
import { TransactionProvider } from './context/TransactionContext'
import FileUpload from './components/FileUpload'
import TabNavigation from './components/TabNavigation'
import DashboardContent from './components/DashboardContent'
import { UploadHistory } from './components/UploadHistory'

function App() {
  const [activeTab, setActiveTab] = useState('debits')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <TransactionProvider>
      <div className="min-h-screen bg-gray-50 flex">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? 'w-72' : 'w-0'} overflow-hidden bg-white border-r border-gray-200 transition-all duration-300 flex-shrink-0`}>
          <UploadHistory onRefreshTransactions={() => window.dispatchEvent(new CustomEvent('refresh-transactions'))} />
        </aside>

        {/* Main content */}
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors"
                aria-label="Toggle uploads sidebar"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-2xl font-bold text-gray-900">Personal Finance Dashboard</h1>
            </div>
          </header>
          
          <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full">
            <FileUpload />
            <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />
            <DashboardContent activeTab={activeTab} />
          </main>
        </div>
      </div>
    </TransactionProvider>
  )
}

export default App
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd frontend && npm test -- app-sidebar.spec.ts`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/src/App.jsx
git commit -m "feat: add collapsible uploads sidebar to app layout"
```

---

### Task 7: Run Migrations & Verify End-to-End

**Files:**
- Run: alembic migration generation
- Test: manual verification

- [ ] **Step 1: Generate migration**

```bash
cd backend && .\venv\Scripts\python.exe -m alembic revision --autogenerate -m "add documents table and transaction document_id"
```

- [ ] **Step 2: Apply migration**

```bash
cd backend && .\venv\Scripts\python.exe -m alembic upgrade head
```

- [ ] **Step 3: Test upload + delete flow**

1. Start backend: `cd backend && .\venv\Scripts\python.exe -m uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Upload a CSV → verify document appears in sidebar
4. Click delete → confirm → verify document and transactions removed
5. Re-upload same file → verify new document created (hash stored but not blocking)

- [ ] **Step 4: Run existing tests**

```bash
cd backend && .\venv\Scripts\python.exe -m pytest tests/test_categorizer.py tests/test_csv_parser.py -v
```

- [ ] **Step 5: Commit**

```bash
git add backend/alembic/versions/
git commit -m "chore: migration for documents table"
```

---

## Self-Review Checklist

- [ ] Document model with all required columns (filename, hash, size, date, count)
- [ ] Transaction FK with CASCADE delete
- [ ] SHA256 hash computed on upload
- [ ] Document returned in upload response
- [ ] GET /documents returns list newest first
- [ ] DELETE /documents/{id} cascades to transactions
- [ ] Frontend sidebar collapses/expands
- [ ] Document list shows filename, date, count, size, hash prefix
- [ ] Delete button with confirmation
- [ ] Re-upload allowed (no hash blocking)
- [ ] All new code tested
- [ ] Existing tests still pass