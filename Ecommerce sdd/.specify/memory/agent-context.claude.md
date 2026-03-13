# ShopEasy Ecommerce — Development Guidelines (Claude)

Auto-generated from all feature plans. Last updated: 2026-03-01

## Active Technologies

| Concern | Choice | Version |
|---------|--------|---------|
| Language | Python | 3.14 |
| Web framework | Flask | 3.0.3 |
| ORM | Flask-SQLAlchemy | 3.1.1 |
| Database | SQLite | (ships with Python) |
| Frontend | Bootstrap 5.3 CDN + Vanilla JS | 5.3.3 |
| Templates | Jinja2 | (ships with Flask) |
| Config | python-dotenv | 1.0.1 |
| Testing | pytest + pytest-flask | 8.3.5 / 1.3.0 |
| Cart storage | Flask session (signed cookie) | (ships with Flask) |

## Project Structure

```text
app/
├── __init__.py              ← create_app(); register blueprints + context processor
├── models.py                ← Product model (SQLAlchemy)
├── routes/
│   ├── catalog.py           ← catalog_bp: GET /, GET /products/<id>
│   └── cart.py              ← cart_bp: GET /cart, POST /cart/add,
│                               POST /cart/update, POST /cart/remove/<id>
├── templates/
│   ├── base.html            ← Bootstrap layout; navbar with cart badge
│   ├── catalog/
│   │   ├── index.html       ← Product grid + search
│   │   └── detail.html      ← Product detail + Add to Cart
│   ├── cart/
│   │   └── index.html       ← Cart page: items, quantities, subtotal
│   └── errors/
│       ├── 404.html
│       └── 500.html
└── static/
    ├── css/store.css
    ├── js/search.js
    └── images/placeholder.png

seeds/products.py            ← 12 seed products across 4 categories
tests/
├── conftest.py              ← pytest fixtures (app, client, seeded_client, cart_client)
├── test_catalog_routes.py   ← 14 route tests (Feature 001)
├── test_models.py           ← 4 model unit tests (Feature 001)
└── test_cart_routes.py      ← 11+ cart route tests (Feature 002)
run.py                       ← Entry point: create_all() + seed_if_empty() + run()
```

## Commands

```bash
# Start dev server (auto-seeds on first run)
python run.py

# Run all tests
pytest tests/ -v --tb=short

# Run only cart tests
pytest tests/test_cart_routes.py -v

# Seed database manually
python seeds/products.py

# Install dependencies
pip install -r requirements.txt

# Switch to cart feature branch
git checkout 002-shopping-cart
```

## Code Style

- PEP 8; max line length 100 chars
- All DB queries via SQLAlchemy ORM (no raw SQL)
- Blueprint pattern: one blueprint per feature (`catalog_bp`, `cart_bp`)
- Flask session cart: always set `session.modified = True` after nested dict write
- Cart prices stored as `str(Decimal)` — never `float` (precision)
- PRG pattern for all form POST routes (redirect after post)

## Recent Changes

### Feature 002: Shopping Cart (2026-03-01 — in progress)
- Session-based cart (flask.session signed cookie)
- Routes: GET /cart, POST /cart/add, POST /cart/update, POST /cart/remove/<id>
- Context processor: `cart_count` available in all templates
- No new database tables required

### Feature 001: Product Catalog (2026-03-01 — complete)
- Flask app factory + SQLAlchemy Product model (9 columns)
- Routes: GET / (catalog + search), GET /products/<id> (detail)
- 18 pytest tests passing
- 12 seed products across 4 categories

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
