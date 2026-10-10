# Graph Report - Personal-Finance-Automation-main  (2026-10-08)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 435 nodes · 834 edges · 28 communities (18 shown, 10 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 41 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `73c07f7e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- v1/upload.py
- react
- AsyncClient
- categorize_transactions
- Category
- parse_csv
- schemas/category.py
- env.py
- package.json
- frontend/package.json
- alembic
- devDependencies
- vitest.config.js
- update_transaction_category
- async_client
- async_client
- dependencies
- scripts
- clean_db
- @playwright/test
- AsyncSession
- get
- BaseModel

## God Nodes (most connected - your core abstractions)
1. `Category` - 36 edges
2. `Transaction` - 22 edges
3. `react` - 21 edges
4. `categorize_transactions()` - 18 edges
5. `parse_csv()` - 18 edges
6. `get_expense_summary()` - 16 edges
7. `upload_csv()` - 15 edges
8. `Keyword` - 14 edges
9. `TestCSVParser` - 13 edges
10. `TestCategorizer` - 12 edges

## Surprising Connections (you probably didn't know these)
- `upload_csv()` --uses--> `Document`  [INFERRED]
  backend/app/api/v1/upload.py → backend/app/models/document.py
- `test_document_columns()` --uses--> `Document`  [INFERRED]
  backend/tests/test_document_model.py → backend/app/models/document.py
- `test_document_model_exists()` --uses--> `Document`  [INFERRED]
  backend/tests/test_document_model.py → backend/app/models/document.py
- `add_keyword()` --uses--> `Keyword`  [INFERRED]
  backend/app/api/v1/categories.py → backend/app/models/keyword.py
- `list_keywords()` --uses--> `Keyword`  [INFERRED]
  backend/app/api/v1/categories.py → backend/app/models/keyword.py

## Import Cycles
- None detected.

## Communities (28 total, 10 thin omitted)

### Community 0 - "v1/upload.py"
Cohesion: 0.10
Nodes (38): asyncio, get_db(), AsyncSession, delete_document(), list_documents(), AsyncSession, delete, get (+30 more)

### Community 1 - "react"
Cohesion: 0.10
Nodes (20): App(), CategoryManager(), DashboardContent(), ExpensePieChart(), FileUpload(), SummaryTable(), TabNavigation(), TransactionTable() (+12 more)

### Community 2 - "AsyncClient"
Cohesion: 0.07
Nodes (27): AsyncClient, asyncio, Test that Uncategorized category cannot be deleted., Tests for Category Keywords API endpoints., Test listing keywords for a category., Test adding a keyword to a category., Test adding duplicate keyword fails., Test listing transactions when empty. (+19 more)

### Community 3 - "categorize_transactions"
Cohesion: 0.08
Nodes (22): categorize_transactions(), get_significant_words(), keyword_match(), normalize_text(), DataFrame, Extract significant words from text (length >= min_length)., Check if keyword matches details using word-based matching. A keyword matches…, Categorize transactions using keyword matching (case-insensitive). Matches if… (+14 more)

### Community 4 - "Category"
Cohesion: 0.12
Nodes (25): Any, add_keyword(), create_category(), delete_category(), list_categories(), list_keywords(), AsyncSession, delete (+17 more)

### Community 5 - "parse_csv"
Cohesion: 0.10
Nodes (16): parse_csv(), DataFrame, Parse CSV content with flexible column detection., Test parsing a basic CSV with standard columns., Test that empty CSV raises appropriate error., Test CSV with only headers and no data., Test parsing amounts with commas (e.g., 18,551.62)., Test parsing amounts with currency symbols. (+8 more)

### Community 6 - "schemas/category.py"
Cohesion: 0.17
Nodes (24): AsyncSession, post, upload_csv(), CategoryBase, CategoryCreate, CategoryRead, Config, KeywordBase (+16 more)

### Community 7 - "env.py"
Cohesion: 0.11
Nodes (16): ast, Config, Settings, BaseSettings, add_keyword_to_category(), categorize_transactions(), load_transactions(), main() (+8 more)

### Community 8 - "package.json"
Cohesion: 0.09
Nodes (21): author, description, devDependencies, jsdom, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, vitest (+13 more)

### Community 9 - "frontend/package.json"
Cohesion: 0.10
Nodes (20): author, description, jsdom, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event, vitest, keywords (+12 more)

### Community 11 - "devDependencies"
Cohesion: 0.15
Nodes (13): devDependencies, autoprefixer, jsdom, @playwright/test, postcss, tailwindcss, @tailwindcss/postcss, @testing-library/jest-dom (+5 more)

### Community 12 - "vitest.config.js"
Cohesion: 0.20
Nodes (7): localStorageMock, { defineConfig }, react, ref_testing_library_jest_dom, vite, @vitejs/plugin-react, ref_vitest

### Community 13 - "update_transaction_category"
Cohesion: 0.25
Nodes (9): AsyncSession, extract_keyword(), get_expense_summary(), list_transactions(), Extract a clean canonical keyword from transaction details. Normalizes by: -…, update_transaction_category(), date, get (+1 more)

### Community 14 - "async_client"
Cohesion: 0.25
Nodes (8): async_client(), clean_db(), db_session(), AsyncSession, fixture, Create a fresh database session for each test., Clean up database before and after each test., Create an async HTTP client for testing with database session override.

### Community 15 - "async_client"
Cohesion: 0.25
Nodes (8): async_client(), clean_db(), db_session(), AsyncSession, fixture, Create a fresh database session for each test., Clean up database before and after each test., Create an async HTTP client for testing with database session override.

### Community 16 - "dependencies"
Cohesion: 0.22
Nodes (9): dependencies, axios, date-fns, react, react-dom, react-hot-toast, recharts, vite (+1 more)

### Community 17 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, serve, test, test:coverage, test:run, test:ui

### Community 18 - "clean_db"
Cohesion: 0.33
Nodes (6): clean_db(), db_session(), AsyncSession, fixture, Create a fresh database session for each test., Clean up database before and after each test.

## Knowledge Gaps
- **72 isolated node(s):** `Config`, `Config`, `TransactionContext`, `api`, `autoprefixer` (+67 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 208 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Category` connect `Category` to `v1/upload.py`, `AsyncClient`, `update_transaction_category`, `schemas/category.py`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `parse_csv()` connect `parse_csv` to `v1/upload.py`, `schemas/category.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `categorize_transactions()` connect `categorize_transactions` to `v1/upload.py`, `parse_csv`, `schemas/category.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Category` (e.g. with `add_keyword()` and `create_category()`) actually correct?**
  _`Category` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Transaction` (e.g. with `upload_csv()` and `get_expense_summary()`) actually correct?**
  _`Transaction` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Config`, `TransactionContext` to the rest of the system?**
  _72 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `v1/upload.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._