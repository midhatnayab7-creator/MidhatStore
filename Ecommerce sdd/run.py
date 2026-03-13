import os
from app import create_app, db
from app.models import Product

app = create_app()


def seed_if_empty():
    """Seed the database with initial data if it's empty."""
    if Product.query.count() == 0:
        print("Database is empty — running seed script...")
        from seeds.products import seed_products
        seed_products()
        print("Seeding complete.")


with app.app_context():
    db.create_all()
    seed_if_empty()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
