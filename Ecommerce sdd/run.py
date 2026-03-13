import os
from app import create_app, db
from app.models import Product

app = create_app()

_seeded = False

@app.before_request
def ensure_db():
    global _seeded
    if not _seeded:
        db.create_all()
        from seeds.products import SEED_PRODUCTS
        expected = len([p for p in SEED_PRODUCTS if p.get("is_active", True)])
        actual = Product.query.filter_by(is_active=True).count()
        if actual < expected:
            from seeds.products import seed_products
            seed_products()
        _seeded = True

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        from seeds.products import SEED_PRODUCTS, seed_products
        expected = len([p for p in SEED_PRODUCTS if p.get("is_active", True)])
        actual = Product.query.filter_by(is_active=True).count()
        if actual < expected:
            seed_products()
    app.run(debug=True, port=5000)
