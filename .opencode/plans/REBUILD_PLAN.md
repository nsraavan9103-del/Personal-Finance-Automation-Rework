# Strategic Rebuild Plan: Personal Finance Automation

## Project Overview
Rebuild the existing Streamlit-based finance dashboard as a full-stack application using FastAPI (Python) + PostgreSQL + React (Vite) + Tailwind CSS, maintaining exact 1:1 feature parity with beginner-friendly code.

## Current Features Analysis

1. CSV Upload - Upload bank statement CSV files (P0)
2. Transaction Parsing - Parse Date, Details, Amount, Currency, Debit/Credit, Status (P0)
3. Auto-Categorization - Keyword-based matching against stored categories (P0)
4. Category Management - Add/remove custom categories dynamically (P0)
5. Manual Categorization - Edit transaction categories inline (teaches keywords) (P0)
6. Debit/Credit Tabs - Separate views for Expenses (Debits) vs Payments (Credits) (P0)
7. Expense Summary - Grouped totals by category with sorting (P0)
8. Pie Chart Visualization - Plotly pie chart of expenses by category (P0)
9. Data Persistence - Categories saved to categories.json (P0)
10. Local-Only Privacy - No external data transmission (P0)

## Target Tech Stack
- Backend: FastAPI 0.110+, SQLAlchemy 2.0+, Pydantic 2.0+, PostgreSQL 15+
- Frontend: React 18+, Vite 5+, Tailwind CSS 3.4+, Axios 1.6+, Recharts 2.12+, date-fns 3.0+

## Backend Structure
backend/
  app/
    main.py, core/, models/, schemas/, api/v1/, services/
  requirements.txt, alembic.ini, migrations/

## Frontend Structure
frontend/
  src/
    main.jsx, App.jsx, components/, hooks/, services/, utils/, pages/
  package.json, vite.config.js, tailwind.config.js

## Database Schema
- categories (id, name, created_at)
- keywords (id, category_id, keyword, created_at)
- transactions (id, date, details, amount, currency, debit_credit, status, category_id, uploaded_at)

## API Endpoints
- GET/POST /api/v1/categories
- DELETE /api/v1/categories/{id}
- GET/POST /api/v1/categories/{id}/keywords
- GET /api/v1/transactions, GET /api/v1/transactions/summary
- PUT /api/v1/transactions/{id}/category
- POST /api/v1/upload/csv

## Implementation Phases
Phase 1 (Week 1): Backend foundation - FastAPI setup, models, migrations, services, endpoints
Phase 2 (Week 2): Frontend foundation - React+Vite+Tailwind, components, hooks, API integration
Phase 3 (Week 3): Integration & polish - E2E testing, edge cases, responsive design, parity verification
Phase 4 (Future): Docker, Auth, Budgets, Export features

## Beginner Code Guidelines
- Simple functions over classes
- Clear dependency injection
- Custom hooks for data fetching
- Minimal abstraction layers

## Success Criteria
- All 10 P0 features working identically to Streamlit version
- Sample CSV produces identical category totals
- Categories persist across restarts (PostgreSQL)
- Manual categorization teaches keywords correctly
- Responsive UI works on desktop/tablet
- No console errors in browser
- API docs accessible at /docs
