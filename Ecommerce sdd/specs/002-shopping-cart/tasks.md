# Tasks: 002 — Shopping Cart

**Feature**: Shopping Cart (Session-Based)
**Branch**: `002-shopping-cart`
**Date**: 2026-03-01
**Total Tasks**: 34 across 6 phases

**Design docs**: plan.md · spec.md · data-model.md · contracts/cart-routes.md · research.md

**TDD Rule** (Constitution Principle I — NON-NEGOTIABLE):
Write test → confirm RED → implement → confirm GREEN → refactor

---

## Phase 1: Setup (T001–T003)

**Purpose**: Create the blueprint skeleton and directory structure.
No user story work begins until this phase is complete.

- [x] T001 Create `app/templates/cart/` directory (empty, marks template namespace)
- [x] T002 Create `app/routes/cart.py` with empty `cart_bp = Blueprint('cart', __name__)` and no routes yet
- [x] T003 Register `cart_bp` in `app/__init__.py` inside `create_app()` alongside existing `catalog_bp`

**Checkpoint**: `python run.py` starts without import errors; no routes added yet

---

## Phase 2: Foundation — Shared Prerequisites (T004–T006)

**Purpose**: Cart helper logic and test fixtures that ALL user story phases depend on.

⚠️ **CRITICAL**: No user story work begins until this phase is complete.

- [x] T004 Add `cart_count` context processor to `app/__init__.py`:
  ```python
  @app.context_processor
  def inject_cart_count():
      cart = session.get('cart', {})
      count = sum(item['quantity'] for item in cart.values())
      return {'cart_count': count}
  ```
  Import `session` from `flask` at top of `__init__.py`.

- [x] T005 Add cart helper functions at top of `app/routes/cart.py`:
  - `get_cart()` → returns `session.get('cart', {})`
  - `save_cart(cart)` → sets `session['cart'] = cart; session.modified = True`
  These keep route handlers clean.

- [x] T006 Update `tests/conftest.py` — add two new fixtures:
  - `cart_client(app)`: test client with one item pre-loaded in session
    (`product_id=1, name="Laptop Pro 15", price="999.99", quantity=1, image_file="placeholder.png"`)
  - `empty_cart_client(app)`: test client with explicit empty `session['cart'] = {}`

**Checkpoint**: `pytest tests/ -v` still passes (18/18 from Feature 001); fixtures importable

---

## Phase 3: US1 — Add Product to Cart (T007–T016)

**Goal**: Shopper adds an in-stock product from the detail page; cart session is updated.

**Independent Test**: Navigate to a product detail page → click "Add to Cart"
→ redirected to `/cart` → product appears with `quantity=1` and correct price.

### Tests for US1 — Write FIRST, confirm RED before implementing ⚠️

- [x] T007 [P] [US1] Write test in `tests/test_cart_routes.py`:
  `test_add_to_cart_adds_item_to_session` — POST `/cart/add` with valid `product_id`;
  assert redirect 302; assert product_id key exists in `session['cart']`

- [x] T008 [P] [US1] Write test in `tests/test_cart_routes.py`:
  `test_add_same_product_twice_increments_quantity` — POST `/cart/add` twice with
  same product_id; assert `session['cart'][str(id)]['quantity'] == 2`

- [x] T009 [P] [US1] Write test in `tests/test_cart_routes.py`:
  `test_add_out_of_stock_product_is_rejected` — POST `/cart/add` with product whose
  `stock=0`; assert redirect does NOT add to cart (cart remains empty)

- [x] T010 [P] [US1] Write test in `tests/test_cart_routes.py`:
  `test_add_to_cart_quantity_capped_at_stock` — POST `/cart/add` with `quantity=9999`
  for product with `stock=5`; assert `session['cart'][str(id)]['quantity'] == 5`

- [x] T011 [P] [US1] Write test in `tests/test_cart_routes.py`:
  `test_cart_count_context_processor_reflects_session` — after adding 2 items
  (qty 1 each), GET `/`; assert `b'2'` in response.data (badge visible in navbar HTML)

> **GATE**: Run `pytest tests/test_cart_routes.py -v` — all 5 US1 tests MUST FAIL (RED) before proceeding.

### Implementation for US1

- [x] T012 [US1] Implement `POST /cart/add` route in `app/routes/cart.py`:
  1. Parse `product_id` (int) and `quantity` (int, default 1) from `request.form`
  2. Query `db.get_or_404(Product, product_id)` — 404 if not found
  3. If `not product.is_active`: abort(404)
  4. If `product.stock == 0`: flash("Out of stock", "danger"); redirect back to detail page
  5. Load cart via `get_cart()`; str key = `str(product_id)`
  6. If key in cart: `cart[key]['quantity'] += quantity` else: create new CartItem dict
  7. Cap: `cart[key]['quantity'] = min(cart[key]['quantity'], product.stock)`
  8. If capped: flash warning
  9. `save_cart(cart)`; flash("Added to cart!", "success"); redirect `/cart`

- [x] T013 [US1] Update `app/templates/catalog/detail.html` — add "Add to Cart" form:
  - `<form method="POST" action="{{ url_for('cart.add') }}">`
  - Hidden `<input name="product_id" value="{{ product.id }}">`
  - Hidden `<input name="quantity" value="1">`
  - Submit button: `<button type="submit" {% if product.stock == 0 %}disabled{% endif %} class="btn btn-success">`
  - Show "Out of Stock" text on button when disabled
  - Display flash messages from `get_flashed_messages(with_categories=True)` (or add to `base.html`)

- [x] T014 [US1] Update `app/templates/base.html` — cart badge in navbar:
  - Add cart link: `<a href="{{ url_for('cart.index') }}" class="btn btn-outline-light position-relative">`
  - Badge: `<span class="badge bg-danger position-absolute">{{ cart_count }}</span>`
  - Only show badge if `cart_count > 0`
  - Add flash message display block in `base.html` (alerts for all pages)

- [x] T015 [US1] Add `from flask import session` import to `app/__init__.py` (needed by context processor)

- [x] T016 [US1] Run `pytest tests/test_cart_routes.py::TestUS1 -v` (or by function names) — all 5 US1 tests MUST be GREEN

**Checkpoint**: US1 tests GREEN; shopper can add products to cart from detail page; badge visible in navbar

---

## Phase 4: US2 — View Cart Contents (T017–T022)

**Goal**: Shopper views a dedicated `/cart` page showing all items, quantities,
line totals, and a correct subtotal.

**Independent Test**: Add 2 products → navigate to `/cart` → both appear with
correct names, unit prices, quantities, and the subtotal equals sum of line totals.

### Tests for US2 — Write FIRST, confirm RED ⚠️

- [x] T017 [P] [US2] Write test in `tests/test_cart_routes.py`:
  `test_cart_page_returns_200` — GET `/cart` returns HTTP 200

- [x] T018 [P] [US2] Write test in `tests/test_cart_routes.py`:
  `test_cart_page_shows_item_name_and_price` — using `cart_client` fixture;
  GET `/cart`; assert product name and price appear in response.data

- [x] T019 [P] [US2] Write test in `tests/test_cart_routes.py`:
  `test_cart_subtotal_is_correct` — cart with 1 item at price 999.99 qty 2;
  GET `/cart`; assert "1999.98" in response.data

- [x] T020 [P] [US2] Write test in `tests/test_cart_routes.py`:
  `test_empty_cart_shows_empty_message` — GET `/cart` with no session items;
  assert "empty" in response.data (case-insensitive)

> **GATE**: Run US2 tests — all 4 MUST FAIL (RED) before proceeding.

### Implementation for US2

- [x] T021 [US2] Implement `GET /cart` route in `app/routes/cart.py`:
  1. `cart = get_cart()`
  2. For each item in cart: check `Product.is_active` and `Product.stock` (warn if changed)
  3. Compute `subtotal = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())`
  4. Build `product_warnings` list (products now inactive or oos)
  5. Render `cart/index.html` with `cart_items`, `subtotal`, `product_warnings`
  Import `Decimal` from `decimal` at top of `cart.py`

- [x] T022 [US2] Create `app/templates/cart/index.html`:
  - Extends `base.html`; block title "Your Cart"
  - **Empty state**: `{% if not cart_items %}` → Bootstrap alert "Your cart is empty"
    + link to `{{ url_for('catalog.index') }}`
  - **Items table**: Bootstrap table — columns: Image | Product | Unit Price | Qty | Line Total | Actions
  - Each row: `{{ item.image_file }}` img, name, `${{ item.price }}`,
    quantity (inline update form — POST /cart/update), `${{ line_total }}`,
    Remove button (POST /cart/remove/<id>)
  - **Order summary card**: Subtotal `${{ "%.2f"|format(subtotal) }}`
  - Display flash messages at top of page (using `get_flashed_messages`)

**Checkpoint**: US1 + US2 tests all GREEN; cart page shows items and correct subtotal

---

## Phase 5: US3 — Update and Remove Cart Items (T023–T029)

**Goal**: Shopper can change quantities or remove individual items from the cart page.

**Independent Test**: Add item qty 1 → change to qty 3 on cart page → line total
updates; remove item → cart shows empty state.

### Tests for US3 — Write FIRST, confirm RED ⚠️

- [x] T023 [P] [US3] Write test in `tests/test_cart_routes.py`:
  `test_update_quantity_changes_session` — using `cart_client`; POST `/cart/update`
  with `product_id=1, quantity=3`; assert `session['cart']['1']['quantity'] == 3`

- [x] T024 [P] [US3] Write test in `tests/test_cart_routes.py`:
  `test_update_quantity_zero_removes_item` — POST `/cart/update` with `quantity=0`;
  assert `str(product_id)` NOT in `session['cart']`

- [x] T025 [P] [US3] Write test in `tests/test_cart_routes.py`:
  `test_update_quantity_capped_at_stock` — POST `/cart/update` with `quantity=9999`;
  assert quantity == product.stock

- [x] T026 [P] [US3] Write test in `tests/test_cart_routes.py`:
  `test_remove_item_deletes_from_session` — using `cart_client`; POST `/cart/remove/1`;
  assert redirect 302; assert `'1'` NOT in `session['cart']`

> **GATE**: Run US3 tests — all 4 MUST FAIL (RED) before proceeding.

### Implementation for US3

- [x] T027 [US3] Implement `POST /cart/update` route in `app/routes/cart.py`:
  1. Parse `product_id` (int) and `quantity` (int) from `request.form`
  2. Load `cart = get_cart()`; key = `str(product_id)`
  3. If key not in cart: redirect `/cart` (no-op)
  4. If `quantity <= 0`: `cart.pop(key)`; flash "Item removed"; `save_cart(cart)`; redirect
  5. Else: look up `product.stock`; `cart[key]['quantity'] = min(quantity, product.stock)`
  6. If capped: flash "Only N available — quantity adjusted", "warning"
  7. `save_cart(cart)`; redirect `/cart`

- [x] T028 [US3] Implement `POST /cart/remove/<int:product_id>` route in `app/routes/cart.py`:
  1. Load `cart = get_cart()`
  2. `cart.pop(str(product_id), None)` — silent no-op if not present
  3. `save_cart(cart)`; flash "Item removed from cart.", "info"; redirect `/cart`

- [x] T029 [US3] Update `app/templates/cart/index.html` — add interactive forms per row:
  - **Update form** (inline): `<form method="POST" action="{{ url_for('cart.update') }}">`
    with hidden `product_id`, number input `quantity` (min=0, max=product_stock or 999),
    "Update" submit button
  - **Remove form**: `<form method="POST" action="{{ url_for('cart.remove', product_id=item.product_id) }}">`
    with a "Remove" button (no extra inputs needed — product_id in URL)

**Checkpoint**: ALL US1 + US2 + US3 tests GREEN; full cart workflow functional in browser

---

## Phase 6: Polish & Verification (T030–T034)

**Purpose**: Full test suite green; browser walkthrough; responsive check; PHR.

- [x] T030 Run full pytest suite: `pytest tests/ -v --tb=short`
  **Expected**: All tests PASS (18 from Feature 001 + new cart tests)

- [x] T031 Execute `quickstart.md` walkthrough (all 10 steps):
  - `python run.py`; complete all 10 manual verification steps
  - Confirm flash messages appear correctly on add, update, remove, oos
  - Confirm out-of-stock product has disabled button

- [x] T032 Responsive check: DevTools → 375px on `/cart` page
  - Cart table stacks or scrolls gracefully; no broken layout

- [x] T033 Merge readiness check:
  - `git status` — no untracked secrets or `.env` files
  - `git diff main --name-only` — review all changed files
  - All changed files are expected (see plan.md file list)

- [x] T034 Create PHR at `history/prompts/002-shopping-cart/005-shopping-cart-tasks.tasks.prompt.md`

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    └── Phase 2 (Foundation — BLOCKS all stories)
            ├── Phase 3 (US1 — P1) ← MVP stopping point
            │       └── Phase 4 (US2 — P2)
            │               └── Phase 5 (US3 — P3)
            │                       └── Phase 6 (Polish)
```

### User Story Dependencies

- **US1 (P1)**: Depends only on Phase 1+2 — independently testable and deliverable
- **US2 (P2)**: Depends on Phase 1+2 only; integrates with US1's cart session data
- **US3 (P3)**: Depends on Phase 1+2 + US2's cart page template (adds forms to it)

### Within Each Story

1. Tests MUST be written and confirmed FAIL before any implementation
2. Helper functions / blueprint setup before routes
3. Routes before templates
4. Templates before integration test of the full page

### Parallel Opportunities

Within Phase 3 (US1), all 5 test tasks (T007–T011) can run in parallel:
```bash
# All US1 test tasks can be written in parallel (different test functions):
Task T007: test_add_to_cart_adds_item_to_session
Task T008: test_add_same_product_twice_increments_quantity
Task T009: test_add_out_of_stock_product_is_rejected
Task T010: test_add_to_cart_quantity_capped_at_stock
Task T011: test_cart_count_context_processor_reflects_session
```

Within Phase 4 (US2), all 4 test tasks (T017–T020) can run in parallel.
Within Phase 5 (US3), all 4 test tasks (T023–T026) can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundation (T004–T006)
3. Complete Phase 3: US1 (T007–T016)
4. **STOP and VALIDATE**: `pytest tests/test_cart_routes.py -k US1 -v` GREEN
5. Manual check: add a product → cart badge updates → `/cart` redirect works
6. Deploy/demo: shoppers can now add products to a cart ✅

### Full Incremental Delivery

```
Setup + Foundation → US1 (add to cart) → US2 (view cart) → US3 (update/remove) → Polish
```

Each story delivers independently testable, demonstrable value.

---

## Task Summary

| Phase | Tasks | Story | Key Deliverable |
|-------|-------|-------|----------------|
| 1 | T001–T003 | — | Blueprint skeleton registered |
| 2 | T004–T006 | — | Context processor + fixtures ready |
| 3 | T007–T016 | US1 | Add to cart + navbar badge |
| 4 | T017–T022 | US2 | Cart page with subtotal |
| 5 | T023–T029 | US3 | Update qty + remove item |
| 6 | T030–T034 | — | Full suite green + manual verify |

**Total**: 34 tasks | **Parallel opportunities**: 13 tasks | **MVP stopping point**: after T016
