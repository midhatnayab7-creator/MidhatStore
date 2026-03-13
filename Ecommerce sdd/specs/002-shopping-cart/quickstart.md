# Quickstart: 002 — Shopping Cart

**Date**: 2026-03-01
**Branch**: `002-shopping-cart`

This guide validates the shopping cart feature works end-to-end after
implementation. Run these steps in order.

---

## Prerequisites

```bash
# 1. Ensure you are on the correct branch
git checkout 002-shopping-cart

# 2. Activate virtualenv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Ensure requirements are installed
pip install -r requirements.txt
```

---

## Step 1: Run Tests (TDD Gate)

```bash
pytest tests/ -v --tb=short
```

**Expected**: All tests PASS (including new `tests/test_cart_routes.py`)

---

## Step 2: Start the Dev Server

```bash
python run.py
```

**Expected output**:
```
Database is empty — running seed script...
Seeded 12 products (11 active, 1 inactive).
 * Running on http://127.0.0.1:5000
```

---

## Step 3: US1 — Add Product to Cart

1. Open `http://127.0.0.1:5000`
2. Click any product card → "View Details"
3. Click "Add to Cart" button
4. **Expected**: Redirected to `/cart`; product appears with quantity 1
5. **Expected**: Navbar shows badge with `1`

---

## Step 4: US1 — Add Same Product Again

1. Navigate back to the same product detail page
2. Click "Add to Cart" again
3. **Expected**: Cart shows quantity `2` for that product (not two rows)
4. **Expected**: Navbar badge shows `2`

---

## Step 5: US2 — View Cart Subtotal

1. Add a second (different) product to the cart
2. Navigate to `/cart`
3. **Expected**: Two rows, each with unit price × quantity as line total
4. **Expected**: Subtotal = sum of all line totals
5. **Expected**: Subtotal is mathematically correct

---

## Step 6: US3 — Update Quantity

1. On the cart page, change quantity of an item to `3`
2. Submit the update
3. **Expected**: Line total updates to unit price × 3
4. **Expected**: Subtotal updates accordingly

---

## Step 7: US3 — Remove Item

1. Click "Remove" on any cart item
2. **Expected**: Item disappears from cart
3. **Expected**: Subtotal recalculates
4. Remove all items
5. **Expected**: "Your cart is empty" message + link to catalog

---

## Step 8: Out-of-Stock Guard

1. Find "Hooded Zip Sweatshirt" (seeded with `stock=0`)
2. Navigate to its detail page
3. **Expected**: "Add to Cart" button is disabled (greyed out) or absent

---

## Step 9: Cart Persists in Session

1. Add items to cart
2. Navigate to several pages (catalog, detail pages, `/cart`)
3. **Expected**: Cart contents remain consistent across navigation
4. Close browser tab entirely; reopen `http://127.0.0.1:5000/cart`
5. **Expected**: Cart is empty (session ended)

---

## Step 10: Responsive Check

1. Open browser DevTools → 375px mobile width
2. Navigate to `/cart` with items
3. **Expected**: Cart table/list is readable, no horizontal scroll

---

## Validation Passed ✅

If all 10 steps pass, the Shopping Cart feature is ready for `/sp.tasks`
or direct implementation merge.
