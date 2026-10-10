# Implementation Plan: Personal Finance Automation Rebuild

## Decisions Confirmed
- **Database**: PostgreSQL 15+ installed locally
- **Keyword Matching**: Exact match (case-insensitive) — details must equal keyword exactly
- **CSV Parser**: Flexible — handle different bank statement formats
- **Frontend Proxy**: Vite proxy for /api → backend (port 5173 → 8000)
- **Verification Baseline**: Captured (see below)
- **Approach**: Scaffold backend + frontend together

## Verification Baseline (Golden Master)
- Total transactions: 50 (36 Debits, 14 Credits)
- Debit total: 25,897.91 AED — all currently Uncategorized
- Credit total: 144,288.30 AED
- Categories.json: {'Uncategorized': []} — empty keywords

## Phase 0: Environment Setup (Day 0)
- [ ] Create project directories: backend/, frontend/
- [ ] PostgreSQL: Create database 'finance_db' and user
- [ ] Python venv: backend/venv
- [ ] Node.js: Verify v18+ installed
- [ ] Create .env files for both projects

## Phase 1: Backend Foundation (Days 1-3)

### 1.1 Project Structure & Config
- backend/
  - app/
    - __init__.py
    - main.py                 # FastAPI app, CORS, routers
    - core/
      - config.py             # Settings (DATABASE_URL, CORS_ORIGINS)
      - database.py           # SQLAlchemy async engine, session
    - models/
      - __init__.py
      - category.py           # Category ORM
      - keyword.py            # Keyword ORM
      - transaction.py        # Transaction ORM
    - schemas/
      - __init__.py
      - category.py           # Pydantic CategoryCreate, CategoryRead
      - keyword.py            # KeywordCreate, KeywordRead
      - transaction.py        # TransactionCreate, TransactionRead, TransactionSummary
      - upload.py             # UploadResponse
    - api/
      - __init__.py
      - deps.py               # get_db dependency
      - v1/
        - __init__.py
        - categories.py       # CRUD + keywords
        - transactions.py     # List, summary, update category
        - upload.py           # POST /csv
    - services/
      - __init__.py
      - csv_parser.py         # Flexible CSV parsing
      - categorizer.py        # Exact keyword matching
      - summary.py            # Aggregation logic
  - requirements.txt
  - alembic.ini
  - migrations/

### 1.2 Database Models
- Category: id, name (unique), created_at
- Keyword: id, category_id (FK, cascade), keyword (unique per category), created_at
- Transaction: id, date, details, amount, currency, debit_credit, status, category_id (FK, SET NULL), uploaded_at
- Indexes on: date, debit_credit, category_id, keyword

### 1.3 Services (Core Logic)
- **csv_parser.py**: 
  - Detect columns flexibly (case-insensitive header matching)
  - Required: date, details, amount, debit_credit
  - Optional: currency, status
  - Parse date formats: DD MMM YYYY, YYYY-MM-DD, DD/MM/YYYY
  - Clean amounts: remove commas, currency symbols
  - Return list of dicts

- **categorizer.py** (exact match, case-insensitive):
  - Load all keywords from DB into dict: {keyword_lower: category_id}
  - For each transaction: if details.lower().strip() in keyword_map → category_id
  - Else: uncategorized_id

- **summary.py**:
  - Filter debits, group by category_id, sum amount, sort desc
  - Join with category names

### 1.4 API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/categories | List all categories |
| POST | /api/v1/categories | Create category |
| DELETE | /api/v1/categories/{id} | Delete (400 if Uncategorized) |
| GET | /api/v1/categories/{id}/keywords | List keywords |
| POST | /api/v1/categories/{id}/keywords | Add keyword |
| GET | /api/v1/transactions | List (query: debit_credit, date_from, date_to, limit, offset) |
| GET | /api/v1/transactions/summary | Category totals for debits |
| PUT | /api/v1/transactions/{id}/category | Update category + auto-add keyword |
| POST | /api/v1/upload/csv | Upload CSV → parse → categorize → save → return summary |

### 1.5 Alembic & Seed
- Initial migration creates all tables
- Seed script: INSERT Uncategorized category (id=1)

### 1.6 Tests
- Unit: categorizer exact match logic
- Unit: CSV parser with sample + edge cases
- Integration: Full upload → categorize → summary flow

## Phase 2: Frontend Foundation (Days 4-6)

### 2.1 Project Setup
- frontend/ (Vite + React 18 + TypeScript optional)
- Dependencies: react, react-dom, axios, recharts, date-fns, react-hot-toast
- Dev: vite, tailwindcss, postcss, autoprefixer, vitest
- Tailwind config: custom colors, forms plugin
- Vite proxy: '/api' → 'http://localhost:8000'

### 2.2 API Layer
- src/services/api.js: Axios instance with baseURL=''
- Methods: getCategories, createCategory, deleteCategory, addKeyword, getTransactions, getSummary, updateTransactionCategory, uploadCSV

### 2.3 Custom Hooks
- useCategories: fetch, create, delete
- useTransactions: fetch with filters
- useSummary: fetch expense summary
- useUpload: mutation for CSV upload

### 2.4 Components
| Component | Purpose |
|-----------|---------|
| Layout | Page wrapper, header |
| FileUpload | Drag-drop CSV, progress, toasts |
| CategoryManager | List categories, add form, delete buttons (protect Uncategorized) |
| TransactionTable | Editable table (date, details, amount, category select), save button |
| SummaryTable | Category totals, formatted amounts |
| ExpensePieChart | Recharts PieChart, tooltip, responsive |
| TabNavigation | Tabs: Expenses (Debits) / Payments (Credits) |

### 2.5 Pages
- Dashboard.jsx: Composes all components
  - FileUpload at top
  - TabNavigation
  - Debits tab: CategoryManager + TransactionTable + SummaryTable + ExpensePieChart
  - Credits tab: TransactionTable (read-only) + Total Payments metric

### 2.6 Styling & UX
- Modern color palette (slate/indigo/emerald)
- Responsive: mobile (<640), tablet (640-1024), desktop (>1024)
- Loading skeletons, error toasts, empty states
- AED currency formatting, DD/MM/YYYY dates
- Smooth transitions, focus states

## Phase 3: Integration & Polish (Days 7-8)

### 3.1 End-to-End Verification
- [ ] Upload sample CSV → 50 transactions saved
- [ ] All 36 debits initially Uncategorized (matches baseline)
- [ ] Manual categorize 1 transaction → keyword learned → refresh → auto-categorized
- [ ] Add category → persists → available in dropdown
- [ ] Delete category → transactions set to Uncategorized
- [ ] Summary totals match baseline after manual categorization
- [ ] Pie chart data matches summary table
- [ ] Credits tab shows 14 transactions, total 144,288.30 AED
- [ ] Page refresh → all data persists in PostgreSQL

### 3.2 Edge Cases
- Empty CSV, missing columns, invalid dates, duplicate categories
- Network errors → user-friendly toasts
- Large files (streaming parse if needed)

### 3.3 Documentation
- README: setup, run commands, env vars
- API docs: Swagger at /docs
- Database setup guide

## Phase 4: Future Enhancements (Post-MVP)
- Docker Compose
- JWT Authentication
- Budget tracking
- Recurring detection
- Export CSV/PDF
- Multi-account
- Dark mode

## File-by-File Creation Order (for execution)

### Backend (18 files)
1. backend/requirements.txt
2. backend/.env.example
3. backend/app/core/config.py
4. backend/app/core/database.py
5. backend/app/models/__init__.py
6. backend/app/models/category.py
7. backend/app/models/keyword.py
8. backend/app/models/transaction.py
8. backend/app/schemas/__init__.py
9. backend/app/schemas/category.py
10. backend/app/schemas/keyword.py
11. backend/app/schemas/transaction.py
12. backend/app/schemas/upload.py
13. backend/app/api/deps.py
14. backend/app/api/v1/__init__.py
15. backend/app/api/v1/categories.py
16. backend/app/api/v1/transactions.py
17. backend/app/api/v1/upload.py
18. backend/app/services/csv_parser.py
19. backend/app/services/categorizer.py
20. backend/app/services/summary.py
21. backend/app/main.py
22. backend/alembic.ini
23. backend/migrations/env.py (after alembic init)
24. backend/tests/test_categorizer.py
25. backend/tests/test_csv_parser.py

### Frontend (22 files)
1. frontend/package.json
2. frontend/vite.config.js
3. frontend/tailwind.config.js
4. frontend/postcss.config.js
5. frontend/index.html
6. frontend/src/main.jsx
7. frontend/src/App.jsx
8. frontend/src/index.css
9. frontend/src/services/api.js
10. frontend/src/hooks/useCategories.js
11. frontend/src/hooks/useTransactions.js
12. frontend/src/hooks/useSummary.js
13. frontend/src/hooks/useUpload.js
11. frontend/src/components/Layout.jsx
12. frontend/src/components/FileUpload.jsx
13. frontend/src/components/CategoryManager.jsx
14. frontend/src/components/TransactionTable.jsx
15. frontend/src/components/SummaryTable.jsx
16. frontend/src/components/ExpensePieChart.jsx
17. frontend/src/components/TabNavigation.jsx
18. frontend/src/components/ui/Button.jsx
19. frontend/src/components/ui/Input.jsx
20. frontend/src/components/ui/Select.jsx
21. frontend/src/pages/Dashboard.jsx

## Success Criteria (Final)
- [ ] All 10 P0 features working identically to Streamlit
- [ ] Sample CSV produces identical totals after categorization
- [ ] Categories + keywords persist in PostgreSQL across restarts
- [ ] Manual categorization teaches keywords (exact match)
- [ ] Responsive UI, no console errors
- [ ] API docs at http://localhost:8000/docs

## Next Step
Approve this plan → Begin Phase 0 (Environment Setup)
