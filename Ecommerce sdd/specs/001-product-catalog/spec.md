# Feature Spec: 001 — Product Catalog

**Feature**: Product Catalog (Browse, Search, Detail)
**Stage**: spec
**Date**: 2026-03-01
**Priority**: P1 (MVP core feature)

---

## Overview

Enable shoppers to browse all available products, search by keyword, and view
full details for any individual product. This is the foundation of the MVP
ecommerce store — no auth, no cart, no checkout in this feature.

---

## User Stories

### US1 — Browse All Products (P1)
> As a shopper, I want to see all available products in a visual grid so that
> I can discover what the store offers.

**Acceptance Criteria:**
- [ ] AC1.1: `GET /` returns HTTP 200
- [ ] AC1.2: All active products appear on the page (name, price, image, category)
- [ ] AC1.3: Products are displayed as Bootstrap cards in a responsive grid
- [ ] AC1.4: Page includes a navbar with store name and search bar
- [ ] AC1.5: Inactive products (`is_active=False`) are NOT shown

### US2 — Search Products by Keyword (P2)
> As a shopper, I want to search for products by keyword so that I can quickly
> find what I'm looking for without scrolling through everything.

**Acceptance Criteria:**
- [ ] AC2.1: `GET /?q=keyword` returns HTTP 200
- [ ] AC2.2: Only products whose name OR description match the keyword are shown
- [ ] AC2.3: Search is case-insensitive
- [ ] AC2.4: If no products match, a "No products found" message is displayed
- [ ] AC2.5: The search term is preserved in the search input after submission
- [ ] AC2.6: Empty search (`?q=`) shows all products (same as no query param)

### US3 — View Product Detail (P3)
> As a shopper, I want to view a product's full details (description, price,
> stock, category) so that I can make an informed purchase decision.

**Acceptance Criteria:**
- [ ] AC3.1: `GET /products/<id>` returns HTTP 200 for a valid product ID
- [ ] AC3.2: Page displays: name, description, price, category, stock, image
- [ ] AC3.3: `GET /products/99999` returns HTTP 404 with a friendly error page
- [ ] AC3.4: Detail page has a "Back to catalog" link to `/`
- [ ] AC3.5: Out-of-stock badge displayed when `stock == 0`

---

## Functional Requirements

| ID  | Requirement                                                              | Story |
|-----|--------------------------------------------------------------------------|-------|
| FR1 | System displays all `is_active=True` products on the home page           | US1   |
| FR2 | Each product card shows: image, name, category badge, price, "View" link | US1   |
| FR3 | Search filters products by keyword in name OR description (case-insensitive) | US2 |
| FR4 | Search preserves query string in URL and input box                       | US2   |
| FR5 | Empty/missing `q` param returns full catalog (no filter applied)         | US2   |
| FR6 | Product detail page shows all product fields                             | US3   |
| FR7 | Invalid product ID returns HTTP 404 with back-link                       | US3   |
| FR8 | Out-of-stock products still visible but labeled "Out of Stock"           | US3   |

---

## Non-Functional Requirements

| ID   | Requirement                                              | Target         |
|------|----------------------------------------------------------|----------------|
| NFR1 | Home page loads in < 500ms with ≤ 20 products            | p95 < 500ms    |
| NFR2 | All database queries use parameterized statements        | Zero SQL injection |
| NFR3 | Mobile-responsive layout (Bootstrap grid)                | 375px min width|
| NFR4 | No secrets in source code                                | `.env` only    |

---

## Out of Scope (MVP)

- User authentication / registration / login
- Shopping cart / checkout / payment
- Product image upload UI
- Pagination (acceptable for ≤ 20 products)
- Admin CRUD interface
- Product reviews / ratings

---

## Success Criteria

| SC  | Criterion                                               | Verified By          |
|-----|---------------------------------------------------------|----------------------|
| SC1 | All pytest tests pass with zero failures                | `pytest tests/ -v`   |
| SC2 | Seed data (12 products, 3+ categories) loads correctly  | Browser walkthrough  |
| SC3 | Search filters results correctly for keyword "laptop"   | Manual test          |
| SC4 | `/products/99999` returns 404 with friendly page        | Browser + pytest     |
| SC5 | Layout works at 375px mobile width (single column)      | Browser DevTools     |

---

## Data Model

**Table: `products`**

| Column       | Type           | Constraints              |
|--------------|----------------|--------------------------|
| id           | INTEGER        | PK, auto-increment       |
| name         | VARCHAR(120)   | NOT NULL                 |
| description  | TEXT           | NOT NULL                 |
| price        | NUMERIC(10,2)  | NOT NULL, > 0            |
| category     | VARCHAR(60)    | NOT NULL                 |
| stock        | INTEGER        | NOT NULL, default 0      |
| image_file   | VARCHAR(200)   | default 'placeholder.png'|
| is_active    | BOOLEAN        | default True             |
| created_at   | DATETIME       | auto-set on insert       |
