# Personal Finance Automation - Improvement Plan

## Overview
This document outlines identified improvements and optimizations for the Personal Finance Automation application, organized by priority and impact.

---

## Critical (High Impact, Low Effort)

### 1. Fix API Base URL Inconsistency
**Files:** frontend/src/context/TransactionContext.jsx, frontend/src/hooks/useDocuments.js
**Issue:** TransactionContext uses /api while useDocuments uses /api/v1. The Vite proxy rewrites /api to /api/v1, but direct calls bypass this.
**Fix:** Standardize on /api everywhere and let Vite proxy handle the rewrite.

`javascript
// In TransactionContext.jsx - already correct
const API_BASE = '/api'

// In useDocuments.js - CHANGE from '/api/v1' to '/api'
const API_BASE = '/api'
`

### 2. Deduplicate Keyword Extraction Logic
**Files:** backend/app/api/v1/transactions.py (lines 73-104), backend/app/services/categorizer.py (lines 5-41)
**Issue:** Two implementations of keyword extraction/normalization with duplicated corporate suffixes and stop words.
**Fix:** Create a single shared utility module backend/app/utils/keyword_extractor.py with:
- normalize_text(text: str) -> str
- extract_significant_words(text: str) -> set
- extract_keyword(details: str) -> str (canonical keyword for learning)
- keyword_match(keyword: str, details: str) -> bool (matching logic)

### 3. Move Corporate Suffixes/Stop Words to Constants
**Files:** backend/app/api/v1/transactions.py (lines 57-71, 90-101), backend/app/services/categorizer.py (line 18)
**Issue:** Hardcoded sets duplicated in 3 places.
**Fix:** Single source of truth in backend/app/constants/keywords.py:

`python
CORPORATE_SUFFIXES = frozenset({...})
STOP_WORDS = frozenset({...})
MIN_WORD_LENGTH = 3
`

---

## High Impact (Performance & Maintainability)

### 4. Optimize Categorization Performance
**File:** backend/app/services/categorizer.py (lines 43-75)
**Issue:** Uses iterrows() which is slow for large DataFrames. The nested loop (keywords x transactions) is O(nxm).
**Fix Options:
- Vectorized approach: Use df.apply() with pre-compiled keyword patterns
- Trie-based matching: Build a prefix tree for O(details_length) matching
- Batch processing: Use pandas string operations for substring matching

**Quick win:** Replace iterrows() with itertuples() (~2x faster) and pre-compile keyword regex patterns.

`python
# Current: slow
for idx, row in df.iterrows():
    for keyword in sorted_keywords:
        if keyword_match(keyword, row['Details'].lower()):
            ...

# Better: vectorized substring check
import re
patterns = [(re.compile(rf'\b{re.escape(kw)}\b', re.I), cat_id) for kw, cat_id in keyword_map.items()]
# Apply via df['Details'].str.contains() or apply with compiled patterns
`

### 5. Add Caching for Categories/Keywords on Upload
**File:** backend/app/api/v1/upload.py (lines 41-49)
**Issue:** Every upload fetches ALL categories and keywords from DB, even for small CSVs.
**Fix:
- Add in-memory cache with TTL (e.g., functools.lru_cache or cachetools.TTLCache)
- Invalidate cache on category/keyword create/delete
- Or: load keywords once at startup and refresh via event

### 6. Centralize Frontend Data Fetching with React Query
**Files:** All frontend components using useEffect + useState for data fetching
**Issue:** Boilerplate loading/error/refresh logic duplicated across:
- TransactionTable.jsx (fetchTransactions, fetchCategories)
- SummaryTable.jsx (fetchSummary)
- ExpensePieChart.jsx (fetchSummary)
- CategoryManager.jsx (fetchCategories)
- UploadHistory.jsx (useDocuments hook)

**Fix:** Add @tanstack/react-query (React Query v5):
- Replace all useEffect fetch patterns with useQuery
- Automatic caching, deduplication, background refetch
- invalidateQueries replaces manual refreshData() pattern
- Eliminates refreshKey workaround

---

## Medium Impact (Code Quality & DX)

### 7. Add React Error Boundaries
**Missing:** No error boundaries in component tree.
**Fix:** Wrap route-level components with react-error-boundary:
`jsx
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
`

### 8. Centralize Date/Currency Formatting
**Files:** TransactionTable.jsx (lines 72-79), UploadHistory.jsx (lines 24-32), SummaryTable.jsx (line 56)
**Issue:** Duplicate formatDate, formatCurrency, formatSize functions.
**Fix:** Create frontend/src/utils/formatters.js:
`js
export const formatDate = (dateString, locale = 'en-GB') => ...
export const formatCurrency = (amount, currency = 'AED') => ...
export const formatFileSize = (bytes) => ...
`

### 9. Move Hardcoded Colors to Theme/Config
**File:** frontend/src/components/ExpensePieChart.jsx (line 34)
**Issue:** COLORS array hardcoded in component.
**Fix:
- Add to Tailwind config as chartColors or CSS variables
- Or use Recharts' built-in color cycling

### 10. Replace Window Event with Context for Document Refresh
**Files:** FileUpload.jsx (line 82), UploadHistory.jsx (lines 10-16)
**Issue:** Cross-component communication via window.dispatchEvent is fragile.
**Fix:** Add documents state to TransactionContext (or create DocumentContext) and use invalidateQueries from React Query.

### 11. Add Database Connection Pooling for Production
**File:** backend/app/core/database.py (line 10)
**Issue:** NullPool disables connection pooling - fine for dev/testing, bad for production.
**Fix:** Use QueuePool (default) with appropriate pool_size and max_overflow in production config.

---

## Low Impact (Nice to Have)

### 12. Add API Versioning Strategy
**Current:** /api/v1 in paths, but Vite proxy rewrites /api to /api/v1.
**Consider:** Explicit versioning in Accept header or path for future-proofing.

### 13. Add Request Validation Middleware
**Missing:** No global request size limits, rate limiting, or input sanitization middleware.
**Fix:** Add slowapi for rate limiting, fastapi-limiter or middleware for request size.

### 14. Add OpenAPI Documentation Enhancements
**Current:** Basic FastAPI auto-docs.
**Enhance:** Add examples, descriptions, response models to all endpoints.

### 15. Add Frontend Unit Tests
**Current:** Only Playwright E2E tests.
**Add:** Vitest + React Testing Library for component logic (formatters, hooks, utils).

### 16. Add Database Indexes for Common Queries
**Check:** Current indexes in migration 1183047b27d3:
- idx_transactions_debit_credit
- idx_transactions_category
- ix_transactions_date
**Consider:** Composite index on (debit_credit, date) for filtered date-range queries.

### 17. Add Soft Delete for Categories
**Current:** Hard delete with Uncategorized protection.
**Consider:** deleted_at timestamp for audit trail.

---

## Implementation Priority Order

| # | Task | Est. Effort | Impact |
|---|------|-------------|--------|
| 1 | Fix API base URL inconsistency | 5 min | Critical |
| 2 | Deduplicate keyword extraction logic | 30 min | Critical |
| 3 | Move constants to single file | 15 min | Critical |
| 4 | Optimize categorization (itertuples + compiled patterns) | 45 min | High |
| 5 | Add keyword/category caching on upload | 30 min | High |
| 6 | Add React Query | 2-3 hrs | High |
| 7 | Add Error Boundaries | 30 min | Medium |
| 8 | Centralize formatters | 20 min | Medium |
| 9 | Move colors to config | 15 min | Medium |
| 10 | Replace window event with context | 30 min | Medium |
| 11 | Fix connection pooling | 10 min | Medium |
| 12-17 | Remaining items | varies | Low |

---

## Quick Wins (Do First)

1. API URL fix - 5 minutes, eliminates potential production bug
2. Constants deduplication - 15 minutes, prevents drift
3. itertuples() optimization - 15 minutes, 2x categorization speed
4. Connection pool fix - 10 minutes, production readiness

---

## Technical Debt Notes

### Shortcuts Taken (with known ceilings)
- shortcut: extract_keyword in transactions.py duplicates categorizer.py logic, upgrade when keyword logic changes
- shortcut: NullPool for DB connections, upgrade to QueuePool before production deploy
- shortcut: window.dispatchEvent for cross-component sync, upgrade to React Query/context when adding more shared state

### Risk Items
- CSV upload memory: Large files loaded entirely into memory (await file.read()). Consider streaming for >10MB files.
- Keyword matching: Current word-boundary matching may false-positive on partial words. Consider \b boundaries or full-text search.
- No duplicate detection: Same CSV uploaded twice creates duplicate transactions. File hash exists but not checked.

---

## Next Steps

1. Apply Critical fixes (1-3)
2. Implement High Impact items (4-6) - React Query is the biggest refactor
3. Address Medium items incrementally during feature work
4. Track Low items in backlog
