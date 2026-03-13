# API Contracts: 002 — Shopping Cart Routes

**Date**: 2026-03-01
**Pattern**: HTML form POST + PRG (Redirect-After-Post)
**Blueprint**: `cart_bp` (URL prefix: none — routes at root)

---

## Route 1: `GET /cart`

**Purpose**: Display the full cart contents (US2)

**Input**: None (reads from `session['cart']`)

**Output**: HTML page

**Success**: HTTP 200 + rendered `cart/index.html`

**Template context**:
```python
{
    "cart_items": list[dict],   # all CartItem dicts from session
    "subtotal": Decimal,        # sum of (price × quantity) for all items
    "product_warnings": list    # products that are now inactive/oos
}
```

**Behaviour**:
- Reads `session.get('cart', {})`
- For each item in cart, re-checks `Product.is_active` and `Product.stock`
  to surface warnings (edge case: product deactivated after add)
- Computes subtotal from stored prices (not live product prices)
- Empty cart → renders template with `cart_items=[]` and empty-cart message

**Error paths**:
- HTTP 500 on database error (standard Flask error handler)

---

## Route 2: `POST /cart/add`

**Purpose**: Add a product to the cart or increment its quantity (US1)

**Input** (HTML form body):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `product_id` | int | Yes | Must exist and be active |
| `quantity` | int | No | Default: 1 |

**Success**: HTTP 302 redirect → `/cart`

**Failure responses**:

| Condition | Response |
|-----------|----------|
| Product not found or `is_active=False` | 404 |
| `stock == 0` | Redirect `/products/<id>` with flash error "Out of Stock" |
| Quantity > stock | Add at `min(quantity, stock)`; flash warning |
| Invalid `product_id` (non-int) | 400 |

**Behaviour**:
1. Validate product exists and `is_active=True`
2. Validate `stock > 0`
3. Load `session['cart']` (default `{}`)
4. If product already in cart: `cart[str(id)]['quantity'] += quantity`
   (capped at stock)
5. If product not in cart: create new CartItem sub-dict
6. Cap: `cart[str(id)]['quantity'] = min(cart[str(id)]['quantity'], product.stock)`
7. Write back to `session['cart']`; mark `session.modified = True`
8. Flash success message; redirect `/cart`

---

## Route 3: `POST /cart/update`

**Purpose**: Change quantity of an existing cart item (US3)

**Input** (HTML form body):

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `product_id` | int | Yes | Must be in cart |
| `quantity` | int | Yes | 0 = remove item |

**Success**: HTTP 302 redirect → `/cart`

**Behaviour**:
1. Load `session['cart']`
2. If `product_id` not in cart: ignore, redirect `/cart`
3. If `quantity <= 0`: remove item from cart (calls remove logic)
4. If `quantity > 0`: re-validate against current `Product.stock`
   - Set `quantity = min(requested, product.stock)`
   - Flash warning if capped
5. Write session; redirect `/cart`

---

## Route 4: `POST /cart/remove/<int:product_id>`

**Purpose**: Remove a specific item from the cart entirely (US3)

**Input**: `product_id` in URL path

**Success**: HTTP 302 redirect → `/cart`

**Behaviour**:
1. Load `session['cart']`
2. `session['cart'].pop(str(product_id), None)` — no-op if not present
3. `session.modified = True`
4. Flash confirmation "Item removed"; redirect `/cart`

---

## Context Processor: `cart_count`

**Available in all templates** as `{{ cart_count }}`

**Type**: `int`
**Derivation**: `sum(item['quantity'] for item in session.get('cart', {}).values())`

**Registration**: `@app.context_processor` in `app/__init__.py`

**Used in**: `base.html` navbar badge

---

## Flash Message Taxonomy

| Trigger | Category | Message |
|---------|----------|---------|
| Add success | `success` | "Added to cart!" |
| Already in cart (qty incremented) | `info` | "Quantity updated in cart." |
| Out of stock | `danger` | "Sorry, this item is out of stock." |
| Qty capped at stock | `warning` | "Only N available — quantity adjusted." |
| Item removed | `info` | "Item removed from cart." |
| Cart empty at checkout | `warning` | "Your cart is empty." |
