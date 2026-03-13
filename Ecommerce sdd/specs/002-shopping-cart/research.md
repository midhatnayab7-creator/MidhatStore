# Research: 002 — Shopping Cart

**Date**: 2026-03-01
**Branch**: 002-shopping-cart

---

## Decision 1: Cart Storage Mechanism

**Question**: How should cart state be stored without user authentication?

**Decision**: Flask built-in signed-cookie session (`flask.session`)

**Rationale**:
- Zero additional dependencies — `flask.session` ships with Flask 3.x
- Data is stored client-side in a tamper-proof signed cookie (HMAC-SHA1)
  using `SECRET_KEY` — server cannot be spoofed by modified cookies
- Cart data for MVP (≤ 50 items × ~60 bytes per item) fits well under the
  4 KB browser cookie limit (~3 KB worst case)
- Perfectly aligned with Principle II (Smallest Viable Change): no Redis,
  no database table, no extra package needed
- Session expires naturally when the browser closes (satisfies FR-011)

**Alternatives considered**:

| Option | Why Rejected |
|--------|-------------|
| Flask-Session (server-side, filesystem) | Extra dependency; adds complexity; no benefit at MVP scale |
| Flask-Session (Redis) | Requires Redis instance; overkill for a session cart |
| SQLite `carts` table | Requires user identity or anonymous session ID as FK; adds schema migration; overkill without auth |
| localStorage (client-side JS) | Requires API endpoint for stock validation; more complex than session; breaks with no-JS fallback |

---

## Decision 2: Cart Data Structure in Session

**Question**: What shape should the cart dict take inside `session`?

**Decision**: Dict keyed by `str(product_id)`, value is a sub-dict with
captured price, quantity, name, and image.

```python
session['cart'] = {
    "7": {
        "product_id": 7,
        "name": "Laptop Pro 15",
        "price": "999.99",   # stored as string — Decimal not JSON-serializable
        "quantity": 2,
        "image_file": "placeholder.png"
    }
}
```

**Rationale**:
- String keys required — JSON (Flask session codec) requires string keys
- Price stored as string to avoid `Decimal` → JSON serialisation errors
  (SQLAlchemy `Numeric` returns `Decimal`; `float` loses precision)
- Name and image stored at add-time (price-lock principle from spec Assumptions)
- O(1) lookup for add/update/remove by product_id

---

## Decision 3: Cart HTTP Operations

**Question**: Standard form POST or AJAX for cart mutations?

**Decision**: HTML forms with `POST` redirect-after-post (PRG pattern)

**Rationale**:
- Consistent with existing Flask + Vanilla JS stack (no fetch/AJAX needed)
- PRG prevents duplicate submissions on browser back/refresh
- Works without JavaScript (progressive enhancement)
- Simpler to test with Flask test client (no JSON parsing)
- Debounced JS enhancement can be added in Polish phase if desired

---

## Decision 4: Cart Item Count in Navbar

**Question**: How to make cart item count available in ALL templates?

**Decision**: Flask `@app.context_processor` injecting `cart_count` globally

**Rationale**:
- Context processors run before every request and inject variables into
  Jinja2 template context automatically — no need to pass count in every route
- Single source of truth: computed from `session.get('cart', {})` values
- No database query needed — pure session read
- Aligned with Principle VI (Separation of Concerns): count logic lives in
  `app/__init__.py` or `app/routes/cart.py`, not in every individual route

---

## Decision 5: Stock Validation Strategy

**Question**: When should stock be validated — on add, on update, or on both?

**Decision**: Validate on every add AND every update against current `Product.stock`

**Rationale**:
- Stock can change between the time an item was added and the time the cart
  is viewed (other shoppers may buy the last unit)
- Validation on add: reject if `stock == 0`; cap quantity if requested > stock
- Validation on update: cap new quantity to `min(requested_qty, product.stock)`
- Note: cart does NOT reserve stock (out of scope per spec) — validation is
  advisory, not transactional
- If product is deactivated after add: show warning in cart, exclude from
  subtotal (matches spec edge case)

---

## Decision 6: Blueprint and File Layout

**Decision**: New `cart_bp` blueprint in `app/routes/cart.py`

**Rationale**: Consistent with existing `catalog_bp` pattern; isolated feature
module; easy to remove or replace without touching other routes.

**Files to create/modify**:

| File | Type | Reason |
|------|------|--------|
| `app/routes/cart.py` | NEW | Cart blueprint: add, view, update, remove routes |
| `app/templates/cart/index.html` | NEW | Cart page template |
| `app/__init__.py` | MODIFY | Register cart_bp + context processor |
| `app/templates/base.html` | MODIFY | Cart badge in navbar |
| `app/templates/catalog/detail.html` | MODIFY | "Add to Cart" button |
| `tests/test_cart_routes.py` | NEW | All cart route tests |
| `tests/conftest.py` | MODIFY | Add cart-aware fixtures |

**No database schema changes required** — cart is 100% session-based.
