"""
Route tests covering all 3 user stories (US1, US2, US3).
Uses the seeded_client fixture (2 active + 1 inactive product).
"""


# ─────────────────────────────────────────────
# US1 — Browse All Products
# ─────────────────────────────────────────────

class TestUS1BrowseProducts:
    """T011-T014: GET / returns product grid."""

    def test_home_returns_200(self, seeded_client):
        """T011: GET / returns HTTP 200."""
        response = seeded_client.get("/")
        assert response.status_code == 200

    def test_home_shows_all_active_product_names(self, seeded_client):
        """T012: All active product names appear in the response."""
        response = seeded_client.get("/")
        html = response.data.decode()
        assert "Laptop Pro 15" in html
        assert "Cotton T-Shirt" in html

    def test_home_does_not_show_inactive_products(self, seeded_client):
        """T013: Inactive product name does NOT appear in catalog."""
        response = seeded_client.get("/")
        html = response.data.decode()
        assert "Inactive Widget" not in html

    def test_home_contains_bootstrap(self, seeded_client):
        """T014: Layout sanity — Bootstrap CDN link is in the page."""
        response = seeded_client.get("/")
        html = response.data.decode()
        assert "bootstrap" in html.lower()


# ─────────────────────────────────────────────
# US2 — Search Products
# ─────────────────────────────────────────────

class TestUS2SearchProducts:
    """T020-T023: GET /?q=keyword filters results."""

    def test_search_returns_200(self, seeded_client):
        """T020: GET /?q=laptop returns HTTP 200."""
        response = seeded_client.get("/?q=laptop")
        assert response.status_code == 200

    def test_search_filters_by_keyword(self, seeded_client):
        """T020: Search for 'laptop' returns Laptop Pro 15 but not Cotton T-Shirt."""
        response = seeded_client.get("/?q=laptop")
        html = response.data.decode()
        assert "Laptop Pro 15" in html
        assert "Cotton T-Shirt" not in html

    def test_search_is_case_insensitive(self, seeded_client):
        """T021: Search for 'LAPTOP' (uppercase) returns same results."""
        response = seeded_client.get("/?q=LAPTOP")
        html = response.data.decode()
        assert "Laptop Pro 15" in html

    def test_search_no_match_shows_message(self, seeded_client):
        """T022: Search with no matching results shows 'No products found' message."""
        response = seeded_client.get("/?q=zzznomatch")
        assert response.status_code == 200
        html = response.data.decode()
        assert "No products found" in html

    def test_empty_search_returns_all_products(self, seeded_client):
        """T023: GET /?q= (empty) returns all active products."""
        response = seeded_client.get("/?q=")
        assert response.status_code == 200
        html = response.data.decode()
        assert "Laptop Pro 15" in html
        assert "Cotton T-Shirt" in html

    def test_search_description_match(self, seeded_client):
        """Search matches words in description, not just name."""
        response = seeded_client.get("/?q=organic+cotton")
        html = response.data.decode()
        assert "Cotton T-Shirt" in html


# ─────────────────────────────────────────────
# US3 — Product Detail Page
# ─────────────────────────────────────────────

class TestUS3ProductDetail:
    """T026-T029: GET /products/<id> shows detail or 404."""

    def test_detail_valid_id_returns_200(self, seeded_client, app):
        """T026: GET /products/<valid_id> returns HTTP 200."""
        from app.models import Product
        with app.app_context():
            p = Product.query.filter_by(name="Laptop Pro 15").first()
            product_id = p.id

        response = seeded_client.get(f"/products/{product_id}")
        assert response.status_code == 200

    def test_detail_shows_product_fields(self, seeded_client, app):
        """T027: Detail page shows name, price, description, category."""
        from app.models import Product
        with app.app_context():
            p = Product.query.filter_by(name="Laptop Pro 15").first()
            product_id = p.id

        response = seeded_client.get(f"/products/{product_id}")
        html = response.data.decode()
        assert "Laptop Pro 15" in html
        assert "999" in html           # price
        assert "Electronics" in html   # category
        assert "Intel Core i7" in html # description content

    def test_detail_invalid_id_returns_404(self, seeded_client):
        """T028: GET /products/99999 returns HTTP 404."""
        response = seeded_client.get("/products/99999")
        assert response.status_code == 404

    def test_detail_404_contains_404_text_and_back_link(self, seeded_client):
        """T029: 404 response contains '404' text and a back link."""
        response = seeded_client.get("/products/99999")
        html = response.data.decode()
        assert "404" in html
        assert "Catalog" in html or "catalog" in html or "/" in html
