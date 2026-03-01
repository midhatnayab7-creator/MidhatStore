"""
pytest fixtures for ShopEasy test suite.
Uses in-memory SQLite so tests never touch instance/store.db.
"""
import pytest
from app import create_app, db as _db
from app.models import Product


@pytest.fixture(scope="session")
def app():
    """Create a Flask test application with in-memory SQLite."""
    test_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret",
            "WTF_CSRF_ENABLED": False,
        }
    )
    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.drop_all()


@pytest.fixture()
def client(app):
    """Flask test client (empty DB — each test gets a clean slate via seeded_client or direct inserts)."""
    return app.test_client()


@pytest.fixture()
def seeded_client(app):
    """
    Flask test client with 3 pre-loaded products:
      - Product 1: Laptop Pro 15 (Electronics, active, stock=5)
      - Product 2: Cotton T-Shirt (Clothing, active, stock=20)
      - Product 3: Inactive Widget  (Electronics, INACTIVE)
    """
    with app.app_context():
        # Clean slate
        Product.query.delete()
        _db.session.commit()

        p1 = Product(
            name="Laptop Pro 15",
            description="High-performance laptop with Intel Core i7 and 16GB RAM.",
            price=999.99,
            category="Electronics",
            stock=5,
            image_file="placeholder.png",
            is_active=True,
        )
        p2 = Product(
            name="Cotton T-Shirt",
            description="Soft organic cotton t-shirt for everyday wear.",
            price=19.99,
            category="Clothing",
            stock=20,
            image_file="placeholder.png",
            is_active=True,
        )
        p3 = Product(
            name="Inactive Widget",
            description="This product should not appear in the catalog.",
            price=5.00,
            category="Electronics",
            stock=0,
            image_file="placeholder.png",
            is_active=False,
        )
        _db.session.add_all([p1, p2, p3])
        _db.session.commit()

    client = app.test_client()
    yield client

    # Cleanup after test
    with app.app_context():
        Product.query.delete()
        _db.session.commit()


@pytest.fixture()
def cart_client(app):
    """
    Flask test client with:
    - 1 seeded product (Laptop Pro 15, id varies — fetched dynamically)
    - 1 cart item pre-loaded in session for that product
    """
    with app.app_context():
        Product.query.delete()
        _db.session.commit()

        p = Product(
            name="Laptop Pro 15",
            description="High-performance laptop with Intel Core i7 and 16GB RAM.",
            price=999.99,
            category="Electronics",
            stock=5,
            image_file="placeholder.png",
            is_active=True,
        )
        _db.session.add(p)
        _db.session.commit()
        product_id = p.id

    client = app.test_client()
    # Pre-load one cart item into the session
    with client.session_transaction() as sess:
        sess["cart"] = {
            str(product_id): {
                "product_id": product_id,
                "name": "Laptop Pro 15",
                "price": "999.99",
                "quantity": 1,
                "image_file": "placeholder.png",
            }
        }

    yield client, product_id

    with app.app_context():
        Product.query.delete()
        _db.session.commit()


@pytest.fixture()
def empty_cart_client(app):
    """Flask test client with an explicit empty cart in session."""
    with app.app_context():
        Product.query.delete()
        _db.session.commit()

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["cart"] = {}

    yield client

    with app.app_context():
        Product.query.delete()
        _db.session.commit()
