"""
Unit tests for the Product model.
Tests T010 (model creation, defaults, repr).
"""
from app.models import Product
from app import db


def test_product_creation_with_required_fields(app):
    """Product can be created with all required fields."""
    with app.app_context():
        p = Product(
            name="Test Product",
            description="A test description.",
            price=9.99,
            category="TestCat",
            stock=10,
        )
        db.session.add(p)
        db.session.commit()

        fetched = db.session.get(Product, p.id)
        assert fetched is not None
        assert fetched.name == "Test Product"
        assert float(fetched.price) == 9.99
        assert fetched.category == "TestCat"
        assert fetched.stock == 10

        db.session.delete(fetched)
        db.session.commit()


def test_product_defaults(app):
    """Product defaults: is_active=True, image_file='placeholder.png', stock=0."""
    with app.app_context():
        p = Product(
            name="Default Product",
            description="Testing defaults.",
            price=1.00,
            category="Test",
        )
        db.session.add(p)
        db.session.commit()

        fetched = db.session.get(Product, p.id)
        assert fetched.is_active is True
        assert fetched.image_file == "placeholder.png"
        assert fetched.stock == 0
        assert fetched.created_at is not None

        db.session.delete(fetched)
        db.session.commit()


def test_product_repr(app):
    """Product __repr__ includes id and name."""
    with app.app_context():
        p = Product(
            name="Repr Test",
            description="repr test description",
            price=5.00,
            category="Test",
        )
        db.session.add(p)
        db.session.commit()

        r = repr(p)
        assert "Repr Test" in r
        assert str(p.id) in r

        db.session.delete(p)
        db.session.commit()


def test_inactive_product_flag(app):
    """Product can be set as inactive."""
    with app.app_context():
        p = Product(
            name="Inactive Item",
            description="Should not appear in catalog.",
            price=0.01,
            category="Test",
            is_active=False,
        )
        db.session.add(p)
        db.session.commit()

        fetched = db.session.get(Product, p.id)
        assert fetched.is_active is False

        db.session.delete(fetched)
        db.session.commit()
