"""
Cart route tests — covers US1, US2, US3.
Uses cart_client and empty_cart_client fixtures from conftest.py.
TDD: tests written before implementation — each class verified RED then GREEN.
"""
from decimal import Decimal


# ─────────────────────────────────────────────
# US1 — Add Product to Cart
# ─────────────────────────────────────────────

class TestUS1AddToCart:

    def test_add_to_cart_adds_item_to_session(self, app, seeded_client):
        """T007: POST /cart/add adds product to session and redirects."""
        with app.app_context():
            from app.models import Product
            p = Product.query.filter_by(name="Laptop Pro 15").first()
            product_id = p.id

        response = seeded_client.post(
            "/cart/add", data={"product_id": product_id, "quantity": 1},
            follow_redirects=False,
        )
        assert response.status_code == 302

        with seeded_client.session_transaction() as sess:
            assert str(product_id) in sess.get("cart", {})

    def test_add_same_product_twice_increments_quantity(self, app, seeded_client):
        """T008: Adding the same product twice results in quantity=2."""
        with app.app_context():
            from app.models import Product
            p = Product.query.filter_by(name="Laptop Pro 15").first()
            product_id = p.id

        # Clear cart first
        with seeded_client.session_transaction() as sess:
            sess["cart"] = {}

        seeded_client.post("/cart/add", data={"product_id": product_id, "quantity": 1})
        seeded_client.post("/cart/add", data={"product_id": product_id, "quantity": 1})

        with seeded_client.session_transaction() as sess:
            assert sess["cart"][str(product_id)]["quantity"] == 2

    def test_add_out_of_stock_product_is_rejected(self, app, seeded_client):
        """T009: POST /cart/add for out-of-stock product does NOT add to cart."""
        with app.app_context():
            from app.models import Product
            # Inactive Widget has stock=0 and is_active=False — use a fresh oos product
            from app import db as _db
            oos = Product(
                name="OOS Item", description="Out of stock.", price=1.00,
                category="Test", stock=0, is_active=True,
            )
            _db.session.add(oos)
            _db.session.commit()
            oos_id = oos.id

        with seeded_client.session_transaction() as sess:
            sess["cart"] = {}

        seeded_client.post("/cart/add", data={"product_id": oos_id, "quantity": 1})

        with seeded_client.session_transaction() as sess:
            assert str(oos_id) not in sess.get("cart", {})

    def test_add_to_cart_quantity_capped_at_stock(self, app, seeded_client):
        """T010: Quantity requested > stock is capped at product.stock."""
        with app.app_context():
            from app.models import Product
            p = Product.query.filter_by(name="Laptop Pro 15").first()
            product_id = p.id
            stock = p.stock  # 5

        with seeded_client.session_transaction() as sess:
            sess["cart"] = {}

        seeded_client.post("/cart/add", data={"product_id": product_id, "quantity": 9999})

        with seeded_client.session_transaction() as sess:
            assert sess["cart"][str(product_id)]["quantity"] == stock

    def test_cart_count_in_navbar(self, app, seeded_client):
        """T011: cart_count context processor reflects items in session."""
        with app.app_context():
            from app.models import Product
            p = Product.query.filter_by(name="Laptop Pro 15").first()
            product_id = p.id

        with seeded_client.session_transaction() as sess:
            sess["cart"] = {
                str(product_id): {
                    "product_id": product_id, "name": "Laptop Pro 15",
                    "price": "999.99", "quantity": 2, "image_file": "placeholder.png",
                }
            }

        response = seeded_client.get("/")
        assert response.status_code == 200
        # Badge with count=2 must appear somewhere in the HTML
        assert b"2" in response.data


# ─────────────────────────────────────────────
# US2 — View Cart Contents
# ─────────────────────────────────────────────

class TestUS2ViewCart:

    def test_cart_page_returns_200(self, empty_cart_client):
        """T017: GET /cart returns HTTP 200."""
        response = empty_cart_client.get("/cart")
        assert response.status_code == 200

    def test_cart_page_shows_item_name_and_price(self, cart_client):
        """T018: GET /cart shows product name and price from session."""
        client, product_id = cart_client
        response = client.get("/cart")
        html = response.data.decode()
        assert "Laptop Pro 15" in html
        assert "999.99" in html

    def test_cart_subtotal_is_correct(self, app, cart_client):
        """T019: Subtotal = unit_price × quantity for all items."""
        client, product_id = cart_client
        # Reassign full cart dict (qty=2) so Flask session detects the change
        with client.session_transaction() as sess:
            sess["cart"] = {
                str(product_id): {
                    "product_id": product_id,
                    "name": "Laptop Pro 15",
                    "price": "999.99",
                    "quantity": 2,
                    "image_file": "placeholder.png",
                }
            }

        response = client.get("/cart")
        html = response.data.decode()
        assert "1999.98" in html

    def test_empty_cart_shows_empty_message(self, empty_cart_client):
        """T020: GET /cart with empty session shows friendly empty message."""
        response = empty_cart_client.get("/cart")
        html = response.data.decode().lower()
        assert "empty" in html


# ─────────────────────────────────────────────
# US3 — Update and Remove Cart Items
# ─────────────────────────────────────────────

class TestUS3UpdateRemove:

    def test_update_quantity_changes_session(self, app, cart_client):
        """T023: POST /cart/update changes quantity in session."""
        client, product_id = cart_client
        client.post("/cart/update", data={"product_id": product_id, "quantity": 3})

        with client.session_transaction() as sess:
            assert sess["cart"][str(product_id)]["quantity"] == 3

    def test_update_quantity_zero_removes_item(self, app, cart_client):
        """T024: POST /cart/update with quantity=0 removes item from cart."""
        client, product_id = cart_client
        client.post("/cart/update", data={"product_id": product_id, "quantity": 0})

        with client.session_transaction() as sess:
            assert str(product_id) not in sess.get("cart", {})

    def test_update_quantity_capped_at_stock(self, app, cart_client):
        """T025: POST /cart/update caps quantity at product.stock (stock=5)."""
        client, product_id = cart_client
        client.post("/cart/update", data={"product_id": product_id, "quantity": 9999})

        with client.session_transaction() as sess:
            assert sess["cart"][str(product_id)]["quantity"] == 5

    def test_remove_item_deletes_from_session(self, app, cart_client):
        """T026: POST /cart/remove/<id> removes item; returns 302."""
        client, product_id = cart_client
        response = client.post(f"/cart/remove/{product_id}", follow_redirects=False)

        assert response.status_code == 302
        with client.session_transaction() as sess:
            assert str(product_id) not in sess.get("cart", {})
