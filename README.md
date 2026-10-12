# Personal Finance Automation

A full-stack personal finance dashboard built with FastAPI (Python) + React (Vite) + PostgreSQL + Tailwind CSS.

## Features

- **CSV Upload**: Drag-and-drop bank statement CSV upload with flexible column detection
- **Smart Categorization**: Exact keyword matching (case-insensitive) with manual override
- **Keyword Learning**: Manual categorization automatically teaches new keywords
- **Expense Summary**: Category totals with pie chart visualization
- **Category Management**: Add, delete, and protect categories
- **Debit/Credit Tabs**: Separate views for expenses and payments
- **Responsive Design**: Works on mobile, tablet, and desktop

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - Async ORM with PostgreSQL
- **Pydantic v2** - Data validation
- **Alembic** - Database migrations
- **Pandas** - CSV parsing

### Frontend
- **React 18** - Component-based UI
- **Vite** - Fast build tool
- **Tailwind CSS v4** - Utility-first styling
- **Recharts** - Chart visualizations
- **Axios** - HTTP client

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

## Quick Start

### 1. Clone and Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create `backend/.env`:
```env
DATABASE_URL=postgresql://finance_user:CHANGE_ME@localhost:5432/finance_test
CORS_ORIGINS=http://localhost:5173
SECRET_KEY=your-secret-key
DEBUG=true
```

### 3. Setup Database

```bash
# Create database and user in PostgreSQL
psql -U postgres
CREATE DATABASE finance_test;
CREATE USER finance_user WITH PASSWORD 'CHANGE_ME';
GRANT ALL PRIVILEGES ON DATABASE finance_test TO finance_user;
\q

# Run migrations
cd backend
alembic upgrade head

# Seed default categories
python seed_uncategorized.py
```

### 4. Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload
# Server runs on http://127.0.0.1:8000
# API docs at http://127.0.0.1:8000/docs
```

### 5. Setup Frontend

```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:5173
```

## Usage

1. **Upload Statement**: Drag and drop a CSV bank statement
2. **Review Transactions**: View and filter transactions by date/type
3. **Categorize**: Select categories from dropdown - keywords are learned automatically
4. **Manage Categories**: Add custom categories, protect "Uncategorized"
5. **View Summary**: Expense totals by category with pie chart
5. **Switch Tabs**: Toggle between Expenses (Debits) and Payments (Credits)

## CSV Format

Expected columns (case-insensitive, flexible naming):
- **Date**: `DD MMM YYYY`, `YYYY-MM-DD`, `DD/MM/YYYY`, `MM/DD/YYYY`
- **Details/Description**: Transaction description
- **Amount**: Numeric value (commas/currency symbols auto-cleaned)
- **Debit/Credit**: `Debit` or `Credit`
- **Currency** (optional): Defaults to AED
- **Status** (optional): Defaults to SETTLED

Example:
```csv
Date,Details,Amount,Debit/Credit
15 Jan 2024,STARBUCKS,25.50,Debit
16 Jan 2024,SALARY,5000.00,Credit
```

## API Endpoints

### Categories
- `GET /api/v1/categories` - List all categories
- `POST /api/v1/categories` - Create category
- `DELETE /api/v1/categories/{id}` - Delete category (protects Uncategorized)
- `GET /api/v1/categories/{id}/keywords` - List category keywords
- `POST /api/v1/categories/{id}/keywords` - Add keyword

### Transactions
- `GET /api/v1/transactions` - List transactions (with filters)
- `GET /api/v1/transactions/summary` - Expense summary (debits only)
- `PUT /api/v1/transactions/{id}/category` - Update category + teach keyword

### Upload
- `POST /api/v1/upload/csv` - Upload and process CSV

### Health
- `GET /health` - Health check

## Database Schema

- **categories**: id, name, created_at
- **keywords**: id, category_id, keyword, created_at (unique per category)
- **transactions**: id, date, details, amount, currency, debit_credit, status, category_id, uploaded_at

## Development

### Backend
```bash
cd backend
python -m pytest tests/           # Run tests (uses the finance_test_unit database)
alembic revision --autogenerate -m "message"  # New migration
alembic upgrade head              # Apply migrations
```

> Tests never touch `finance_test` (the app's database). They use `finance_test_unit` — create it once as the postgres superuser:
> `CREATE DATABASE finance_test_unit OWNER finance_user;`

### Frontend
```bash
cd frontend
npm run dev       # Development server
npm run build     # Production build
npm run serve     # Preview production build
```

## API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Verification Checklist (1:1 Streamlit Parity)

- [x] CSV upload accepts same format
- [x] Date parsing: DD MMM YYYY format works
- [x] Amount parsing: handles commas (18,551.62)
- [x] Debit/Credit classification matches exactly
- [x] Auto-categorization uses exact keyword matching (case-insensitive, exact match)
- [x] Manual category edit teaches keyword (detail → category)
- [x] Category add/remove persists across reloads
- [x] Uncategorized category cannot be deleted
- [x] Expense summary totals match Streamlit groupby sum
- [x] Pie chart shows same categories and proportions
- [x] Total Payments metric matches Streamlit sum of credits
- [x] AED currency formatting throughout
- [x] Local-only data (no external API calls)

## Architecture

```
personal-finance/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py          # Dependency injection
│   │   │   └── v1/              # API v1 routes
│   │   │       ├── categories.py
│   │   │       ├── transactions.py
│   │   │       └── upload.py
│   │   ├── core/
│   │   │   ├── config.py        # Settings
│   │   │   └── database.py      # DB connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── main.py              # FastAPI app
│   ├── migrations/              # Alembic migrations
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── services/            # API service
│   │   └── main.jsx             # Entry point
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## License

MIT License


