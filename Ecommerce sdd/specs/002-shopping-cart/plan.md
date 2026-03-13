# Implementation Plan: 002 — Shopping Cart

**Branch**: `002-shopping-cart` | **Date**: 2026-03-01
**Spec**: [spec.md](spec.md) | **Research**: [research.md](research.md)

---

## Summary

Add a session-based shopping cart to the ShopEasy Flask store. Shoppers can
add in-stock products from the detail page, view a dedicated cart page showing
quantities and totals, and update or remove items — all without creating an
account. Cart state lives in Flask's signed-cookie session. No database schema
changes are required.

---

## Technical Context

| Concern | Choice |
|---------|--------|
| Language/Version | Python 3.14 (existing `.venv`) |
| Framework | Flask 3.0.3 + Jinja2 (existing) |
| Cart Storage | `flask.session` signed-cookie (built-in, zero new deps) |
| Database | No changes — SQLite `products` table read-only |
| Frontend | Bootstrap 5.3 CDN + Vanilla JS (existing) |
| Testing | pytest 8.x + pytest-flask (existing) |
| HTTP Pattern | HTML form POST + PRG (Redirect-After-Post) |
| New Dependencies | None |

---

## Constitution Check

*GATE: Must pass before implementation begins. Re-check after design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Test-First | ✅ PASS | Tests written before implementation in every phase |
| II. Smallest Viable Change | ✅ PASS | Session-based cart; no new DB table, no new packages |
| III. Security by Default | ✅ PASS | Flask session is HMAC-signed; all DB reads use ORM; inputs validated |
| IV. Flask Application Factory | ✅ PASS | `cart_bp` registered in `create_app()`; context processor via `init_app` pattern |
| V. Readable Code | ✅ PASS | PEP 8; descriptive names; no inline styles |
| VI. Separation of Concerns | ✅ PASS | Routes in `cart.py`; cart logic in route helpers; templates display-only |

**All gates PASS. Implementation may proceed.**

---

## Project Structure

### Documentation (this feature)

```text
specs/002-shopping-cart/
├── spec.md           ← Feature spec (3 user stories, 11 FRs)
├── plan.md           ← This file
├── research.md       ← 6 architectural decisions
├── data-model.md     ← Cart session structure, CartItem fields
├── quickstart.md     ← 10-step end-to-end validation guide
├── checklists/
│   └── requirements.md   ← Spec quality checklist (14/14 PASS)
└── contracts/
    └── cart-routes.md    ← 4 routes + context processor + flash taxonomy
```

### Source Code Changes

```text
MODIFIED:
  app/__init__.py                     ← Register cart_bp + cart_count context processor
  app/templates/base.html             ← Cart badge in navbar
  app/templates/catalog/detail.html   ← "Add to Cart" form + disabled state for oos
  tests/conftest.py                   ← Add cart-aware test fixtures

NEW:
  app/routes/cart.py                  ← cart_bp: GET /cart, POST /cart/add,
                                         POST /cart/update, POST /cart/remove/<id>
  app/templates/cart/
  └── index.html                      ← Cart page: items, quantities, subtotal, empty state
```

---

## Architectural Decisions

### Decision 1: Flask Built-in Session for Cart Storage
- **Chosen**: `flask.session` signed-cookie
- **Rejected**: Flask-Session (server-side), SQLite cart table, localStorage
- **Rationale**: Zero new dependencies; tamper-proof via HMAC; expires with
  browser session (satisfies FR-011); sufficient capacity for MVP (≤ 50 items)
- See [research.md](research.md) Decision 1 for full analysis

### Decision 2: Price Locked at Add-Time
- **Chosen**: Capture `str(product.price)` at add-time in session
- **Rationale**: Prevents cart subtotal from changing under the shopper if
  the admin updates a price; stored as string to survive JSON serialisation
  (`Decimal` is not JSON-serialisable)
- **Trade-off**: Cart may show a lower price than current catalog; acceptable
  for MVP (no checkout in scope)

### Decision 3: PRG Pattern (No AJAX) for Cart Mutations
- **Chosen**: Standard HTML form `POST` → server-side logic → `redirect()`
- **Rationale**: No JavaScript required; prevents double-submission on refresh;
  simpler to test; consistent with existing catalog pattern
- **Trade-off**: Full page reload on every cart action — acceptable for MVP

### Decision 4: Context Processor for Cart Count
- **Chosen**: `@app.context_processor` injecting `cart_count` globally
- **Rationale**: Avoids passing count manually in every route's `render_template`
  call; consistent with Flask best practices; pure session read (no DB query)

---

## API Routes Summary

| Route | Method | FR | Behaviour |
|-------|--------|----|-----------|
| `/cart` | GET | FR-003, FR-004 | View cart; compute subtotal; surface product warnings |
| `/cart/add` | POST | FR-001, FR-002, FR-007, FR-008 | Add/increment item; validate stock |
| `/cart/update` | POST | FR-005, FR-007 | Update quantity; cap at stock; qty=0 → remove |
| `/cart/remove/<id>` | POST | FR-006 | Remove item unconditionally |

**Context processor** (all templates): `cart_count` — total item quantity in cart (FR-010)

---

## Non-Functional Requirements

| NFR | Target | Implementation |
|-----|--------|----------------|
| Performance | Cart page < 1 second (SC-002) | Session read + max 1 Product query per cart item for warnings |
| Security | No session tampering | Flask HMAC-signed session via `SECRET_KEY` |
| Security | No SQL injection | All Product reads via SQLAlchemy ORM |
| Reliability | Subtotal always correct (SC-005) | Computed server-side from session prices; no client-side math |
| Accessibility | Cart count always visible (SC-006) | Navbar context processor on every request |
| Mobile | Cart readable at 375px | Bootstrap responsive table or stacked layout |

---

## Risk Analysis

| Risk | Blast Radius | Mitigation |
|------|-------------|-----------|
| Cookie size exceeds 4 KB with 50 items | Medium — cart silently fails | Tested at MVP scope; 50 items × 80 bytes = 4 KB ceiling. If hit, flash warning "Cart full". |
| `session.modified` not set after in-place dict mutation | Medium — cart changes not saved | Always set `session.modified = True` after any nested dict write |
| Product.stock decreases after item added (oversell risk) | Low — no stock reservation in scope | Warning shown in cart view; user informed; stock enforcement deferred to checkout (out of scope) |

---

## Testing Strategy

**New file**: `tests/test_cart_routes.py`

| Test | User Story | Covers |
|------|-----------|--------|
| `GET /cart` returns 200 empty state | US2 | FR-003, FR-009 |
| `GET /cart` shows items after add | US2 | FR-004 |
| `POST /cart/add` adds item to session | US1 | FR-001 |
| `POST /cart/add` same product increments qty | US1 | FR-002 |
| `POST /cart/add` out-of-stock rejected | US1 | FR-008 |
| `POST /cart/add` qty capped at stock | US1 | FR-007 |
| `POST /cart/update` changes quantity | US3 | FR-005 |
| `POST /cart/update` qty=0 removes item | US3 | FR-006 |
| `POST /cart/remove/<id>` removes item | US3 | FR-006 |
| Subtotal is mathematically correct | US2 | SC-005 |
| Navbar `cart_count` reflects session | US1/US2 | FR-010, SC-006 |

**Fixtures needed in `conftest.py`**:
- `cart_client`: test client with pre-loaded session cart items
- Product fixtures with known prices and stock levels for assertion

---

## Implementation Order (Critical Path)

1. `app/routes/cart.py` — cart blueprint with all 4 routes
2. `app/__init__.py` — register `cart_bp` + context processor
3. `app/templates/cart/index.html` — cart page
4. `app/templates/base.html` — cart badge in navbar
5. `app/templates/catalog/detail.html` — Add to Cart button
6. `tests/test_cart_routes.py` — full test suite (write FIRST, confirm RED)
7. Implement routes until all tests GREEN

📋 **Architectural decision detected**: Session-based cart vs database-backed cart
— Document reasoning and tradeoffs? Run `/sp.adr session-cart-storage`
