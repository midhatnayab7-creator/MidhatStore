# Tasks: 001 — Product Catalog

**Feature**: Product Catalog
**Stage**: tasks
**Date**: 2026-03-01
**Total Tasks**: 38 across 6 phases

**TDD Rule**: Write test → confirm RED → implement → confirm GREEN → refactor

---

## Phase 1: Project Setup (T001–T004)

**Gate**: `import flask` works; all folders exist; `.venv` packages installed

- [x] **T001** — Create `requirements.txt` with: Flask==3.0.3, Flask-SQLAlchemy==3.1.1, python-dotenv==1.0.1, pytest==8.3.5, pytest-flask==1.3.0
- [x] **T002** — Install packages into `.venv`: `pip install -r requirements.txt`
- [x] **T003** — Create `.env.example` with `SECRET_KEY`, `FLASK_ENV`, `DATABASE_URL` placeholders
- [x] **T004** — Create `.gitignore` covering `.env`, `instance/`, `__pycache__`, `*.pyc`, `.venv`, `*.db`

---

## Phase 2: Foundation — App Factory & DB Model (T005–T010)

**Gate**: `db.create_all()` succeeds; seed script runs; model unit tests GREEN

- [x] **T005** — Create `app/__init__.py` with `create_app()` factory:
  - Load config from environment (SECRET_KEY, SQLALCHEMY_DATABASE_URI)
  - Init Flask-SQLAlchemy with `db.init_app(app)`
  - Register `catalog` blueprint
  - Register 404 and 500 error handlers

- [x] **T006** — Create `app/models.py` with `Product` SQLAlchemy model:
  - All 9 columns: id, name, description, price, category, stock, image_file, is_active, created_at
  - `__repr__` returning `<Product id=X name=Y>`

- [x] **T007** — Create `app/routes/__init__.py` (empty, marks as package)

- [x] **T008** — Create `run.py` entry point:
  - Call `create_app()`
  - Call `db.create_all()` within app context
  - Run Flask dev server on port 5000

- [x] **T009** — Create `seeds/products.py` with 12 seed products across 4 categories:
  - Electronics (3), Clothing (3), Kitchen (3), Books (3)
  - Include 1 inactive product (`is_active=False`)
  - Clear existing products before inserting (idempotent)

- [x] **T010** — Create `tests/conftest.py` with fixtures:
  - `app` fixture: in-memory SQLite, TESTING=True
  - `client` fixture: Flask test client
  - `seeded_client` fixture: 3 pre-loaded test products

---

## Phase 3: US1 — Browse All Products (T011–T019)

**Gate**: All US1 pytest tests PASS; product grid visible in browser

### Tests First (write → confirm RED)
- [x] **T011** — Write test: `GET /` returns HTTP 200
- [x] **T012** — Write test: `GET /` shows all seeded product names in response body
- [x] **T013** — Write test: `GET /` does NOT show inactive product names
- [x] **T014** — Write test: Response contains "Bootstrap" (layout sanity check)

### Implementation (make tests GREEN)
- [x] **T015** — Create `app/routes/catalog.py` with `GET /` route:
  - Query `Product.query.filter_by(is_active=True).all()`
  - Handle `?q=` param (empty = no filter)
  - Render `catalog/index.html` with products list

- [x] **T016** — Create `app/templates/base.html`:
  - Bootstrap 5.3 CDN (CSS + JS bundle)
  - Navbar with store name "ShopEasy" and search form (GET, action="/")
  - `{% block content %}` and `{% block title %}` blocks
  - Link to `static/css/store.css`

- [x] **T017** — Create `app/templates/catalog/index.html`:
  - Extends `base.html`
  - Bootstrap responsive grid: `col-12 col-sm-6 col-lg-4`
  - Product card: image, category badge, name, price, "View Details" link
  - Show "No products found" message when list is empty

- [x] **T018** — Create `app/static/css/store.css`:
  - Card hover shadow
  - Consistent card height
  - Placeholder image sizing

- [x] **T019** — Create `app/static/images/placeholder.png` (simple grey placeholder)

---

## Phase 4: US2 — Search Products (T020–T025)

**Gate**: All US2 pytest tests PASS; search filters results in browser

### Tests First
- [x] **T020** — Write test: `GET /?q=laptop` returns only products matching "laptop"
- [x] **T021** — Write test: `GET /?q=LAPTOP` (uppercase) returns same results (case-insensitive)
- [x] **T022** — Write test: `GET /?q=zzznomatch` returns 200 with "No products found" text
- [x] **T023** — Write test: `GET /?q=` (empty string) returns all active products

### Implementation
- [x] **T024** — Update `catalog.py` `GET /` to apply search filter when `q` is non-empty:
  - `Product.name.ilike(f'%{q}%') | Product.description.ilike(f'%{q}%')`
  - Combine with `is_active=True` filter
  - Pass `query=q` to template

- [x] **T025** — Update `catalog/index.html`:
  - Show search query in heading: "Results for 'keyword'" vs "All Products"
  - Pre-fill search input with current query value

---

## Phase 5: US3 — Product Detail Page (T026–T032)

**Gate**: All US3 pytest tests PASS; 404 works for unknown IDs

### Tests First
- [x] **T026** — Write test: `GET /products/1` returns HTTP 200
- [x] **T027** — Write test: `GET /products/1` shows product name, price, description, category
- [x] **T028** — Write test: `GET /products/99999` returns HTTP 404
- [x] **T029** — Write test: 404 response contains "404" text and back-link

### Implementation
- [x] **T030** — Add `GET /products/<int:id>` route to `catalog.py`:
  - Use `db.get_or_404(Product, id)` to auto-404 on missing ID
  - Render `catalog/detail.html`

- [x] **T031** — Create `app/templates/catalog/detail.html`:
  - Full product display: image, name, category, price, stock, description
  - Out-of-stock badge when `stock == 0`
  - "Back to Catalog" link to `/`

- [x] **T032** — Create `app/templates/errors/404.html` and `errors/500.html`:
  - 404: "Page Not Found" heading + back-to-catalog link
  - 500: "Something went wrong" + back-to-home link

---

## Phase 6: Polish & Verification (T033–T038)

**Gate**: Full `pytest` suite green; mobile layout confirmed; run.py starts cleanly

- [x] **T033** — Create `app/static/js/search.js` with optional debounced search (300ms)
- [x] **T034** — Run full pytest suite: `pytest tests/ -v --tb=short` — all tests PASS
- [x] **T035** — Run seed script: `python seeds/products.py` — 12 products inserted
- [x] **T036** — Manual browser test: `python run.py` → open `http://127.0.0.1:5000`
  - Product grid loads
  - Search for "laptop" → filtered
  - Click product → detail page
  - Visit `/products/99999` → 404 page
- [x] **T037** — Responsive check: DevTools → 375px → single column layout
- [x] **T038** — Create PHR at `history/prompts/general/001-mvp-ecommerce-plan.general.prompt.md`

---

## Task Summary

| Phase | Tasks     | Status |
|-------|-----------|--------|
| 1     | T001–T004 | ✅ Done |
| 2     | T005–T010 | ✅ Done |
| 3     | T011–T019 | ✅ Done |
| 4     | T020–T025 | ✅ Done |
| 5     | T026–T032 | ✅ Done |
| 6     | T033–T038 | ✅ Done |
