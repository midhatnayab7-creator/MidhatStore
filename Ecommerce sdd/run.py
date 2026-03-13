import os
from app import create_app, db
from app.models import Product

app = create_app()


def seed_if_needed():
    """Seed the database with initial data if empty or outdated."""
    from seeds.products import SEED_PRODUCTS
    expected = len([p for p in SEED_PRODUCTS if p.get("is_active", True)])
    actual = Product.query.filter_by(is_active=True).count()
    if actual < expected:
        print(f"Database has {actual} active products, expected {expected} — reseeding...")
        from seeds.products import seed_products
        seed_products()
        print("Seeding complete.")


with app.app_context():
    db.create_all()
    seed_if_needed()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
