# Feature Specification: Shopping Cart

**Feature Branch**: `002-shopping-cart`
**Created**: 2026-03-01
**Status**: Draft
**Input**: User description: "Add a shopping cart feature"

---

## Overview

Allow shoppers to collect products they intend to buy into a temporary cart,
review their selections, adjust quantities, and remove items — all without
requiring an account or completing a purchase. The cart persists within a
browser session and acts as the bridge between product browsing and checkout.

---

## User Scenarios & Testing

### User Story 1 — Add Product to Cart (Priority: P1)

As a shopper, I want to add a product to my cart from the product detail page
so that I can collect items I intend to buy before deciding to purchase.

**Why this priority**: Without being able to add items, the cart cannot exist.
This is the single most critical interaction and gates all other cart behaviour.

**Independent Test**: Navigate to any product detail page, click "Add to Cart",
then view the cart — the product appears with quantity 1 and the correct price.

**Acceptance Scenarios**:

1. **Given** a shopper is on a product detail page with stock > 0,
   **When** they click "Add to Cart",
   **Then** the product is added to the cart with quantity 1, and a confirmation
   is shown (e.g., cart icon badge updates or a success message appears).

2. **Given** a shopper adds the same product twice,
   **When** they view the cart,
   **Then** the product appears once with quantity 2 (not as two separate lines).

3. **Given** a product has `stock = 0` (Out of Stock),
   **When** the shopper views the product detail page,
   **Then** the "Add to Cart" button is disabled or absent — the product cannot
   be added.

---

### User Story 2 — View Cart Contents (Priority: P2)

As a shopper, I want to see everything in my cart — product names, images,
quantities, individual prices, and the total cost — so that I can review my
intended purchases before deciding to proceed.

**Why this priority**: A cart is only useful if the shopper can see and
understand what's in it. This is the primary review surface.

**Independent Test**: Add two different products to the cart, navigate to the
cart page — both appear with correct names, images, unit prices, and the
displayed total matches the sum of (unit price × quantity) for all items.

**Acceptance Scenarios**:

1. **Given** a shopper has items in their cart,
   **When** they navigate to the cart page (`/cart`),
   **Then** each item shows: product image, name, unit price, quantity, and
   line total (unit price × quantity).

2. **Given** multiple items in the cart,
   **When** the cart page loads,
   **Then** an order summary shows the subtotal (sum of all line totals) clearly
   displayed.

3. **Given** the cart is empty,
   **When** the shopper navigates to `/cart`,
   **Then** a friendly "Your cart is empty" message is shown with a link back
   to the product catalog.

---

### User Story 3 — Update and Remove Cart Items (Priority: P3)

As a shopper, I want to change the quantity of items in my cart or remove
items entirely so that I can correct my selections before purchasing.

**Why this priority**: Shoppers make mistakes or change their minds. This
reduces friction and abandonment caused by an inability to modify the cart.

**Independent Test**: Add a product with quantity 1, change its quantity to 3
— the line total and subtotal update correctly. Remove the item — it disappears
and the cart shows as empty.

**Acceptance Scenarios**:

1. **Given** a product is in the cart with quantity 1,
   **When** the shopper changes the quantity to 3 and confirms,
   **Then** the line total updates to unit price × 3 and the subtotal updates
   accordingly.

2. **Given** a shopper sets a product quantity to 0 or clicks "Remove",
   **When** the update is confirmed,
   **Then** the item is removed from the cart entirely.

3. **Given** a shopper tries to set a quantity greater than the product's
   available stock,
   **When** they attempt to update,
   **Then** the quantity is capped at the available stock level and the shopper
   is informed of the limit.

---

### Edge Cases

- What happens when a shopper adds a product then the product is deactivated
  (`is_active = False`) before checkout?
  → The item remains visible in the cart but a warning is shown that it is
  no longer available; it is excluded from the subtotal.

- What happens if two browser tabs add different quantities of the same product?
  → Last write wins; the cart reflects the most recent update.

- What happens when the cart is accessed after the browser session ends?
  → The cart is empty (session-based storage; no login, no persistence across
  sessions). This is a known, documented limitation of the MVP scope.

---

## Requirements

### Functional Requirements

- **FR-001**: A shopper MUST be able to add any in-stock, active product to
  the cart from the product detail page.
- **FR-002**: Adding an already-carted product MUST increment its quantity by 1
  rather than creating a duplicate line item.
- **FR-003**: The cart MUST be accessible at a dedicated URL (`/cart`).
- **FR-004**: The cart page MUST display: product image, name, unit price,
  quantity, line total, and overall subtotal.
- **FR-005**: A shopper MUST be able to update the quantity of any cart item
  directly from the cart page.
- **FR-006**: A shopper MUST be able to remove any individual item from the
  cart.
- **FR-007**: Quantity updates MUST be capped at the product's available stock;
  the shopper MUST be informed when the cap is applied.
- **FR-008**: Out-of-stock products (`stock = 0`) MUST NOT be addable to the
  cart; the "Add to Cart" button MUST be disabled on their detail page.
- **FR-009**: An empty cart MUST display a friendly message and a link to the
  product catalog.
- **FR-010**: The number of items in the cart MUST be visible at all times via
  a badge or indicator in the site navigation bar.
- **FR-011**: The cart MUST persist for the duration of the shopper's browser
  session without requiring an account.

### Key Entities

- **Cart**: A temporary container belonging to a browser session. Contains
  zero or more cart items. Has a computed subtotal.
- **CartItem**: A single line in the cart. Linked to one Product. Has a
  quantity (integer ≥ 1) and a unit price (captured at the time of adding).
- **Product** (existing): Source of product data (name, price, stock,
  is_active, image). Read-only from the cart's perspective.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: A shopper can add a product to the cart in 2 or fewer clicks
  from the product detail page.
- **SC-002**: The cart page loads and displays all items within 1 second for
  up to 20 items in the cart.
- **SC-003**: Quantity changes and removals are reflected on the cart page
  within 1 second of confirmation, with no page reload required (or full
  page reload stays under 1 second).
- **SC-004**: 100% of out-of-stock products have a disabled "Add to Cart"
  button — zero such products can be added to the cart.
- **SC-005**: The displayed cart subtotal is mathematically correct (sum of
  unit price × quantity for all items) for every combination of items tested.
- **SC-006**: The cart item count in the navigation bar is accurate after
  every add, update, and remove operation.

---

## Assumptions

- No user authentication is required to use the cart. The cart is tied to
  the browser session only.
- Prices in the cart reflect the price at the time the item was added. If the
  product price changes after adding, the cart price does not update
  automatically (MVP simplification).
- No checkout, payment, or order confirmation is in scope for this feature.
- No cart-to-cart merging (e.g., anonymous → logged-in) is needed (no auth).
- The product catalog (Feature 001) is complete and its `Product` data model
  is the authoritative source for name, price, stock, and active status.
- Cart storage uses the web server's session mechanism (server-side sessions);
  no client-side database or persistent storage is required.
- A maximum cart size of 50 distinct line items is an acceptable limit for MVP.

---

## Out of Scope

- User accounts, login, or registration
- Payment processing or checkout flow
- Order history or order confirmation
- Saved/wishlist carts that persist beyond the session
- Coupon codes, discounts, or promotions
- Shipping cost calculation
- Tax calculation
- Stock reservation (cart does not lock inventory)
