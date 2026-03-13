# Data Model: 002 — Shopping Cart

**Date**: 2026-03-01
**Storage**: Flask signed-cookie session (no database table required)

---

## Entities

### Cart (Session Object)

The cart is not a database record. It lives in `flask.session` for the
duration of the browser session.

**Session key**: `'cart'`
**Type**: `dict[str, CartItem]` — keyed by `str(product_id)`

**Computed properties** (derived, never stored):

| Property | Derivation |
|----------|-----------|
| `item_count` | `sum(item['quantity'] for item in cart.values())` |
| `subtotal` | `sum(Decimal(item['price']) * item['quantity'] for item in cart.values())` |
| `is_empty` | `len(cart) == 0` |

---

### CartItem (Session Sub-object)

One entry in the `session['cart']` dict per distinct product.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `product_id` | `int` | > 0, FK to `products.id` | Also used as dict key (as `str`) |
| `name` | `str` | max 120 chars | Captured at add-time (price-lock) |
| `price` | `str` | Decimal string e.g. "9.99" | Stored as string to survive JSON serialisation |
| `quantity` | `int` | ≥ 1, ≤ product.stock | Capped at product's current stock on update |
| `image_file` | `str` | max 200 chars | Captured at add-time |

**Validation rules**:
- `quantity` MUST be ≥ 1 at all times; setting to 0 triggers removal
- `quantity` MUST NOT exceed `Product.stock` at time of add/update
- `product_id` MUST reference an existing, `is_active=True` Product with `stock > 0`

**State transitions**:
```
[not in cart] --add()--> [in cart, qty=N]
[in cart, qty=N] --update(qty=M)--> [in cart, qty=M]  (M ≥ 1, M ≤ stock)
[in cart, qty=N] --update(qty=0)--> [not in cart]
[in cart, qty=N] --remove()--> [not in cart]
```

---

### Product (Existing — Read-Only)

The `Product` SQLAlchemy model from Feature 001 is the authoritative source.
The cart reads it for stock validation and initial data capture.
The cart NEVER writes to `Product`.

| Column | Used By Cart | Purpose |
|--------|-------------|---------|
| `id` | ✅ | Cart item key |
| `name` | ✅ | Captured at add-time |
| `price` | ✅ | Captured at add-time (Decimal → string) |
| `stock` | ✅ | Validation gate on add/update |
| `is_active` | ✅ | Validation gate: only active products can be added |
| `image_file` | ✅ | Captured at add-time for cart display |
| `description`, `category`, `created_at` | ❌ | Not needed in cart |

---

## Session Layout Example

```json
{
  "cart": {
    "7": {
      "product_id": 7,
      "name": "Laptop Pro 15",
      "price": "999.99",
      "quantity": 2,
      "image_file": "placeholder.png"
    },
    "3": {
      "product_id": 3,
      "name": "Smartphone Stand & Charger",
      "price": "34.99",
      "quantity": 1,
      "image_file": "placeholder.png"
    }
  }
}
```

**Estimated session size** (worst case: 50 items × ~80 bytes): ~4 KB
— within Flask's default signed-cookie session limit.

---

## No Database Migration Required

This feature adds zero new tables. The existing `products` table is unchanged.
The cart lives entirely in the session cookie.
