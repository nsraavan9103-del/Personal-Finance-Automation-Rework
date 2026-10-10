# TODO: Personal Finance Automation Rebuild
- Create backend/ directory structure ~~(completed~~)
- Initialize Python virtual environment ~~(completed~~)
- Create requirements.txt with all dependencies ~~(completed~~)
- Set up .env file for configuration (DATABASE_URL, CORS_ORIGINS) ~~(completed~~)
### Database & Models
- Configure SQLAlchemy async engine in app/core/database.py ~~(completed~~)
- Create Category model (app/models/category.py) ~~(completed~~)
- Create Keyword model (app/models/keyword.py) ~~(completed~~)
- Create Transaction model (app/models/transaction.py) ~~(completed~~)
- Set up Alembic for migrations ~~(completed~~)
- Generate initial migration ~~(completed~~)
- Run migration to create tables ~~(completed~~)
- Create seed script for default Uncategorized category ~~(completed~~)
### Pydantic Schemas
- Category schemas (Create, Read, Update) ~~(completed~~)
- Keyword schemas ~~(completed~~)
- Transaction schemas (Create, Read, Summary) ~~(completed~~)
- CSV Upload response schemas ~~(completed~~)
### Services (Business Logic)
- CSV Parser Service (app/services/csv_parser.py) ~~(completed~~)
  - Parse CSV with pandas
  - Handle date format (DD MMM YYYY)
  - Clean amount values (remove commas)
  - Validate required columns
- Categorizer Service (app/services/categorizer.py) ~~(completed~~)
- Summary Service (app/services/summary.py) ~~(completed~~)
  - Match transaction details to keywords (case-insensitive)
  - Return category_id or Uncategorized
  - Sort by amount descending
### API Endpoints
- Dependency injection (app/api/deps.py) - get_db() ~~(completed~~)
- Categories Router (app/api/v1/categories.py) ~~(completed~~)
  - GET /categories - list all
  - POST /categories - create new
  - DELETE /categories/{id} - delete (protect Uncategorized)
  - GET /categories/{id}/keywords - list keywords
  - POST /categories/{id}/keywords - add keyword
- Transactions Router (app/api/v1/transactions.py) ~~(completed~~)
  - GET /transactions - list with filters (debit/credit, date range)
  - GET /transactions/summary - category totals for debits
  - PUT /transactions/{id}/category - update category + teach keyword
- Upload Router (app/api/v1/upload.py)
### Main App
- Create FastAPI app (app/main.py) ~~(completed~~)
- Configure CORS middleware ~~(completed~~)
- Include all routers with /api/v1 prefix ~~(completed~~)
- Add health check endpoint ~~(completed~~)
### Testing Backend
- Unit tests for categorizer logic
- Unit tests for CSV parser
- Integration tests for API endpoints
- Test with sample_bank_statement.csv
## Phase 2: Frontend Foundation (Week 2)
### Project Setup
- Create frontend/ directory with Vite + React
- Install dependencies (react, react-dom, axios, recharts, date-fns, react-hot-toast)
- Configure Tailwind CSS (tailwind.config.js, postcss.config.js)
- Set up Axios instance (src/services/api.js) with baseURL
### Shared Components
- Layout.jsx - main page wrapper
- Button.jsx - reusable button with variants
- Input.jsx - styled input component
- Select.jsx - styled select dropdown
- LoadingSpinner.jsx
- ErrorMessage.jsx
### Feature Components
- FileUpload.jsx
  - Drag-and-drop zone
  - File validation (CSV only)
  - Upload progress
  - Success/error handling with toasts
- CategoryManager.jsx
  - List categories with delete buttons
  - Add category form
  - Protect Uncategorized from deletion
- TransactionTable.jsx
  - Display transactions in editable table
  - Inline category editing (select dropdown)
  - Save changes button
  - Date formatting (DD/MM/YYYY)
  - Currency formatting (AED)
- SummaryTable.jsx
  - Category totals table
  - Amount formatting
- ExpensePieChart.jsx
  - Recharts PieChart component
  - Tooltip with category name and amount
  - Responsive sizing
- TabNavigation.jsx
  - Two tabs: Expenses (Debits) / Payments (Credits)
  - Active state styling
### Custom Hooks
- useCategories.js - fetch/create/delete categories
- useTransactions.js - fetch transactions with filters
- useUpload.js - handle CSV upload mutation
- useSummary.js - fetch expense summary
### Pages
- Dashboard.jsx - main page composing all components
  - FileUpload at top
  - TabNavigation
  - Debits tab: CategoryManager + TransactionTable + SummaryTable + ExpensePieChart
  - Credits tab: TransactionTable (read-only) + Total Payments metric
### Styling & UX
- Modern color scheme (Tailwind config)
- Responsive breakpoints (mobile, tablet, desktop)
- Loading states for all async operations
- Error toasts with react-hot-toast
- Empty states for no data
- Consistent spacing and typography
## Phase 3: Integration & Polish (Week 3)
### End-to-End Testing
- Upload sample CSV -> verify transactions appear
- Verify auto-categorization matches Streamlit behavior
- Manual categorization -> verify keyword learning works
- Category add/remove -> verify persistence
- Summary totals -> verify match Streamlit exactly
- Pie chart -> verify data matches summary table
- Debits/Credits tabs -> verify correct filtering
- Page refresh -> verify data persists in PostgreSQL
### Edge Cases & Error Handling
- Empty CSV upload
- Invalid CSV format
- Missing required columns
- Duplicate category names
- Delete category with transactions
- Network error handling
- Large file upload handling
### Visual Polish
- Consistent color palette
- Hover/focus states on interactive elements
- Smooth transitions
- Proper form validation feedback
- Currency symbol consistency (AED)
- Date format consistency
### Documentation
- README with setup instructions
- API documentation (Swagger at /docs)
- Environment variable documentation
- Database setup guide
### Performance
- Pagination for transaction lists (if needed)
- Index verification on database
- Bundle size check for frontend
## Phase 4: Optional Enhancements (Future)
- Docker Compose for local development
- User authentication (JWT)
- Budget tracking per category
- Recurring transaction detection
- Export to CSV/PDF
- Multi-account support
- Monthly/yearly comparison views
- Dark mode toggle
## Verification Checklist (1:1 Parity)
- CSV upload accepts same format as Streamlit
- Date parsing: DD MMM YYYY format works
- Amount parsing: handles commas (18,551.62)
- Debit/Credit classification matches exactly
- Auto-categorization uses exact keyword matching (case-insensitive, exact match)
- Manual category edit teaches keyword (detail -> category)
- Category add/remove persists across reloads
- Uncategorized category cannot be deleted
- Expense summary totals match Streamlit groupby sum
- Pie chart shows same categories and proportions
- Total Payments metric matches Streamlit sum of credits
- AED currency formatting throughout
- Local-only data (no external API calls)
## Notes
- Run tests after each phase completion
- Update this TODO as tasks are completed
- Keep Streamlit app running for parallel comparison
- Commit frequently with descriptive messages
