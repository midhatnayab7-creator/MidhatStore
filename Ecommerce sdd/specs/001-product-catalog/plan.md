# Architecture Plan: 001 — Product Catalog

**Feature**: Product Catalog
**Stage**: plan
**Date**: 2026-03-01

---

## 1. Scope and Dependencies

### In Scope
- Flask application factory (`create_app()`)
- SQLAlchemy `Product` model with SQLite backend
- Two routes: `GET /` (catalog + search) and `GET /products/<id>` (detail)
- Jinja2 templates using Bootstrap 5.3
- Seed script (12 products across 3+ categories)
- pytest test suite (10+ tests)

### Out of Scope
- Authentication, cart, checkout, payment
- Image upload, admin panel, pagination
- External APIs or services

### External Dependencies
- Bootstrap 5.3 (CDN — no local install needed)
- Python 3.14 `.venv` (already exists)
- SQLite 3 (ships with Python)

---

## 2. Key Decisions and Rationale

### Decision 1: Flask Application Factory Pattern
**Options considered**: Single-file app, factory pattern, Flask-CLI app
**Chosen**: Application factory (`create_app()` in `app/__init__.py`)
**Rationale**: Enables multiple app instances for testing (each test gets a fresh
in-memory SQLite DB), follows Flask best practices, supports config per environment.

### Decision 2: SQLite for MVP
**Options considered**: PostgreSQL, MySQL, SQLite
**Chosen**: SQLite with file at `instance/store.db`
**Rationale**: Zero configuration, ships with Python, sufficient for MVP with
< 100 products. Migration to PostgreSQL is straightforward via SQLAlchemy if needed.

### Decision 3: SQLAlchemy ORM (no raw SQL)
**Rationale**: Prevents SQL injection, provides parameterized queries by default,
enables easy migration to other databases, readable Pythonic API.

### Decision 4: Vanilla JS + Bootstrap 5.3 CDN
**Rationale**: No build step, no npm, no webpack. Minimal complexity for MVP.
Bootstrap CDN covers responsive layout. Debounced search is optional JS enhancement.

---

## 3. API Contracts

### Route 1: `GET /`
- **Input**: Optional query param `?q=<keyword>` (string, max 200 chars)
- **Output**: HTML page with product grid
- **Success**: HTTP 200
- **Error**: HTTP 500 (database failure)
- **Search logic**: If `q` provided and non-empty, filter products where
  `name ILIKE '%q%' OR description ILIKE '%q%'` on active products only
- **Empty q**: Treat as no filter (return all active products)

### Route 2: `GET /products/<int:id>`
- **Input**: `id` — integer in URL path
- **Output**: HTML page with product detail
- **Success**: HTTP 200
- **Error**: HTTP 404 if product not found or `is_active=False`
- **Flask behavior**: Use `db.get_or_404(Product, id)` for clean 404 handling

### Error Pages
- `404.html`: Friendly "Page not found" with back-to-catalog link
- `500.html`: Friendly "Something went wrong" page

---

## 4. Non-Functional Requirements

| NFR       | Target                    | Implementation                       |
|-----------|---------------------------|--------------------------------------|
| Perf      | < 500ms home page load    | SQLite index on `is_active`          |
| Security  | No SQL injection          | SQLAlchemy ORM (parameterized only)  |
| Security  | No secrets in code        | `.env` + `python-dotenv`             |
| Responsive| Works at 375px            | Bootstrap `col-12 col-md-6 col-lg-4` |
| Testing   | All tests green           | pytest + pytest-flask                |

---

## 5. Data Management

### Schema

```sql
CREATE TABLE products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    price       NUMERIC(10,2) NOT NULL,
    category    VARCHAR(60) NOT NULL,
    stock       INTEGER NOT NULL DEFAULT 0,
    image_file  VARCHAR(200) NOT NULL DEFAULT 'placeholder.png',
    is_active   BOOLEAN NOT NULL DEFAULT 1,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Migration Strategy
- MVP: `db.create_all()` on app startup (development only)
- Future: Flask-Migrate + Alembic for production schema evolution

### Seed Data
- 12 products across 4 categories: Electronics, Clothing, Kitchen, Books
- `seeds/products.py` — standalone script, safe to re-run (clears & reseeds)

---

## 6. Project File Structure

```
app/
├── __init__.py          ← create_app() factory
├── models.py            ← Product model
├── routes/
│   ├── __init__.py
│   └── catalog.py       ← / and /products/<id> routes
├── templates/
│   ├── base.html        ← Bootstrap layout + navbar + search
│   ├── catalog/
│   │   ├── index.html   ← Product grid
│   │   └── detail.html  ← Product detail
│   └── errors/
│       ├── 404.html
│       └── 500.html
└── static/
    ├── css/store.css
    ├── js/search.js
    └── images/placeholder.png

seeds/products.py
tests/
├── conftest.py
├── test_catalog_routes.py
└── test_models.py
run.py
requirements.txt
.env.example
.gitignore
```

---

## 7. Risk Analysis

| Risk                              | Blast Radius | Mitigation                              |
|-----------------------------------|--------------|-----------------------------------------|
| SQLite file permissions on Windows| Medium       | Use `instance/` folder (Flask default)  |
| Bootstrap CDN offline             | Low          | Fallback CSS in `store.css`             |
| Python 3.14 incompatibility       | Low          | Flask 3.x supports 3.9+; tested widely  |

---

## 8. Testing Strategy

- **Unit tests** (`test_models.py`): Product model creation, field defaults, repr
- **Route tests** (`test_catalog_routes.py`):
  - US1: GET / → 200, all products shown
  - US2: GET /?q=keyword → filtered results; GET /?q=nomatch → 0 results message
  - US3: GET /products/1 → 200; GET /products/99999 → 404
- **Fixture**: In-memory SQLite (`TESTING=True`, `SQLALCHEMY_DATABASE_URI=sqlite:///:memory:`)
- **Seeded fixture**: 3 products (Electronics x2, Clothing x1) for route tests

---

## 9. Operational Readiness

- **Dev server**: `python run.py` (Flask debug mode, port 5000)
- **DB init**: `run.py` calls `db.create_all()` then `seed_if_empty()` on startup
- **Logs**: Flask default logging (stdout)
- **Reset DB**: Delete `instance/store.db` and restart
