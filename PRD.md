# Sales CSV Product Requirements Document (PRD)

Repository: `capstone-starter-test`
Source data: `data/sales.csv`

## 1. Summary & Goals
Provide an interactive sales analytics product built on the `data/sales.csv` file so business users can explore revenue, orders, product performance, and fulfillment metrics for decision-making.

Goals
- Deliver an exploratory dashboard (prototype: Streamlit) for filtering, charting, and exporting sales data.
- Validate and canonicalize CSV fields for consistent reporting.
- Provide a clear path to production (data ingestion, API, deployment).

Out of scope for M1: authentication, large-scale data warehousing, or advanced ML models.

## 2. Data contract
Source file: `data/sales.csv` (columns present in file)

Required column types and transforms
- Row ID: integer
- Order ID: string — order-level grouping key
- Order Date: date (parse MM/DD/YYYY -> ISO)
- Ship Date: date (nullable)
- Ship Mode: enum
- Customer ID: string
- Customer Name: string
- Segment: enum
- Country: string
- City: string
- State: string
- Postal Code: string (currently floats like `42420.0` -> convert to string without decimals)
- Region: enum
- Product ID: string
- Category: enum
- Sub-Category: string
- Product Name: string
- Sales: numeric (float) — coerce non-numeric to NaN or 0 by policy

Derived fields
- Order Month (YYYY-MM)
- Order Year
- Order Value = sum(Sales) grouped by `Order ID`
- Shipping Lead Time = (Ship Date - Order Date) in days
- IsHighValueOrder flag (configurable threshold)

Validation rules
- `Order Date` required; rows missing it should be flagged
- `Sales` must be >= 0; negative values flagged
- `Order ID` required for order-level metrics
- Postal codes should be normalized to string

## 3. Personas & user needs
- Sales Manager: monitor revenue by region and time
- Product Manager: identify top-selling products and categories
- Operations: analyze shipping lead times by mode and region
- Business Analyst: export filtered rows for modeling

Sample user stories
- As a Sales Manager I want total sales by month and region so I can track performance.
- As an Analyst I want to download filtered CSVs so I can run custom analysis.

## 4. Features (MVP)
UI components
- KPI row: Total Sales, Orders (unique `Order ID`), Avg Order Value, Filtered Row Count
- Sidebar filters: Order date range, Region, Category, Ship Mode, text search (product/customer)
- Time series: Sales over time (monthly), interactive
- Bar charts: Sales by Region, Sales by Category
- Top N products: Top 10 products by sales (click to filter)
- Shipping analysis: lead time histogram/boxplot by Ship Mode
- Data table: paginated, sortable, downloadable CSV of filtered rows
- Download: filtered CSV

Nice-to-have
- Growth % vs prior period
- Target/benchmark lines
- Export chart images

## 5. KPIs & success metrics
Primary KPIs
- Total Sales (SUM of Sales)
- Orders (unique `Order ID`)
- Avg Order Value (Total Sales / Orders)

Success criteria
- Dashboard loads and applies filters within reasonable time (prototype target < 2s for filters on local dataset)
- Downloaded CSV exactly matches filtered rows
- Charts aggregate correctly; acceptance tests validate sums for sample queries

## 6. Acceptance criteria
- Data parsing: `Order Date` and `Sales` types validated and converted correctly
- All filters apply consistently across charts and table
- Downloaded CSV corresponds to filtered dataset
- Basic responsiveness on common desktop browsers

## 7. Edge cases and data quality
- Postal Code floats (e.g., `42420.0`) — normalize to string without decimals
- Missing/invalid `Order Date` — flag and optionally exclude
- Duplicate `Order ID` rows — group when computing order-level metrics
- Negative `Sales` — flag for review
- Extremely large dataset — prototype uses in-memory pandas; scale by moving data to DB or S3 and paginating

## 8. Implementation notes
Prototype
- Tech: Streamlit + pandas + Altair (prototype included as `app.py` in repo)
- Local dev: `requirements.txt` provided

Production considerations
- Move CSV into a persistent store (Postgres / S3) with scheduled ingestion
- Add an API layer to serve aggregated queries
- Add authentication/authorization for access control

Testing & CI
- Unit tests for parsing rules (dates, sales numeric)
- Integration test ensuring Streamlit app starts and key charts render (smoke test)
- Add pre-commit or CI checks for data schema changes

## 9. Milestones & rollout
- M1 (1–2 days): parsing, KPIs, and core charts (Streamlit prototype) — DONE
- M2 (1 week): shipping analysis, exports, data QA script, basic tests
- M3 (2–3 weeks): data ingestion to DB/S3, API endpoints, Dockerfile + deploy config, access controls

## 10. Next actions (pick one)
- Add small data QA script that validates dates, negative sales, postal code formatting
- Add unit tests for parsing and basic aggregates
- Create a Dockerfile and deploy config for the Streamlit app

---

Document created from initial PRD draft on: 2025-10-01
