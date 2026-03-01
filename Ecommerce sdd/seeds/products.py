"""
Seed script — products across 5 categories with real images.
Safe to re-run: clears existing products first.

Usage:
    python seeds/products.py
    # OR called from run.py on startup when DB is empty
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Unsplash image URLs — free, no auth required
SEED_PRODUCTS = [
    # ── Electronics ────────────────────────────────────────────────────────────
    {
        "name": "Laptop Pro 15",
        "description": (
            "High-performance laptop with 15-inch display, Intel Core i7 processor, "
            "16GB RAM, and 512GB SSD. Perfect for professionals and students."
        ),
        "price": 999.99,
        "category": "Electronics",
        "stock": 10,
        "image_file": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Wireless Earbuds X200",
        "description": (
            "True wireless earbuds with active noise cancellation, 30-hour battery life, "
            "and water-resistant design. Crystal clear audio quality."
        ),
        "price": 79.99,
        "category": "Electronics",
        "stock": 25,
        "image_file": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Smartphone Stand & Charger",
        "description": (
            "Adjustable desk stand with built-in 15W wireless charging. "
            "Compatible with all Qi-enabled smartphones."
        ),
        "price": 34.99,
        "category": "Electronics",
        "stock": 50,
        "image_file": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    # ── Clothing ────────────────────────────────────────────────────────────────
    {
        "name": "Classic Cotton T-Shirt",
        "description": (
            "Soft 100% organic cotton t-shirt, available in multiple colours. "
            "Pre-shrunk and machine washable. Unisex fit."
        ),
        "price": 19.99,
        "category": "Clothing",
        "stock": 100,
        "image_file": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Slim Fit Chino Trousers",
        "description": (
            "Versatile slim-fit chinos made from stretch cotton blend. "
            "Suitable for both casual and semi-formal occasions."
        ),
        "price": 44.99,
        "category": "Clothing",
        "stock": 30,
        "image_file": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Hooded Zip Sweatshirt",
        "description": (
            "Warm fleece-lined hoodie with full-zip closure and two front pockets. "
            "Great for everyday wear in cooler weather."
        ),
        "price": 54.99,
        "category": "Clothing",
        "stock": 0,
        "image_file": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    # ── Kitchen ─────────────────────────────────────────────────────────────────
    {
        "name": "Stainless Steel Knife Set",
        "description": (
            "Professional 8-piece knife set with ergonomic handles and a bamboo storage block. "
            "High-carbon stainless steel blades stay sharp longer."
        ),
        "price": 89.99,
        "category": "Kitchen",
        "stock": 15,
        "image_file": "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Non-Stick Frying Pan 28cm",
        "description": (
            "Heavy-duty aluminium frying pan with PFOA-free non-stick coating. "
            "Compatible with all hob types including induction."
        ),
        "price": 29.99,
        "category": "Kitchen",
        "stock": 40,
        "image_file": "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Electric Kettle 1.7L",
        "description": (
            "Fast-boil 3000W electric kettle with auto shut-off and keep-warm function. "
            "360-degree cordless base with LED indicator."
        ),
        "price": 39.99,
        "category": "Kitchen",
        "stock": 20,
        "image_file": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    # ── Books ───────────────────────────────────────────────────────────────────
    {
        "name": "Python for Everybody",
        "description": (
            "Beginner-friendly introduction to programming using Python 3. "
            "Covers variables, loops, functions, files, and web scraping. "
            "Perfect for absolute beginners."
        ),
        "price": 24.99,
        "category": "Books",
        "stock": 60,
        "image_file": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Clean Code: A Handbook",
        "description": (
            "A must-read guide to writing readable, maintainable software. "
            "Robert C. Martin shares principles, patterns, and best practices "
            "for professional software craftsmanship."
        ),
        "price": 32.99,
        "category": "Books",
        "stock": 45,
        "image_file": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    # ── Fast Food ───────────────────────────────────────────────────────────────
    {
        "name": "Classic Beef Burger",
        "description": (
            "Juicy 200g beef patty with melted cheddar, crispy lettuce, tomato, "
            "pickles, and our signature sauce — all in a toasted brioche bun."
        ),
        "price": 8.99,
        "category": "Fast Food",
        "stock": 50,
        "image_file": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Margherita Pizza 12\"",
        "description": (
            "Stone-baked 12-inch Margherita pizza with San Marzano tomato sauce, "
            "fresh mozzarella, and hand-torn basil leaves. Light, fresh, and delicious."
        ),
        "price": 12.99,
        "category": "Fast Food",
        "stock": 30,
        "image_file": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Crispy Fried Chicken (8pc)",
        "description": (
            "8-piece golden-fried chicken with our secret spice blend. "
            "Extra crispy coating, juicy inside. Served with dipping sauce and coleslaw."
        ),
        "price": 14.99,
        "category": "Fast Food",
        "stock": 40,
        "image_file": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Loaded French Fries (Large)",
        "description": (
            "Crispy golden fries loaded with melted cheese sauce, crispy bacon bits, "
            "jalapeños, and sour cream. The ultimate comfort snack."
        ),
        "price": 5.99,
        "category": "Fast Food",
        "stock": 100,
        "image_file": "https://images.unsplash.com/photo-1576107232684-1279f390859f?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "BBQ Smokehouse Hotdog",
        "description": (
            "Premium beef frankfurter in a soft brioche roll, topped with smoky BBQ sauce, "
            "crispy fried onions, yellow mustard, and sweet relish."
        ),
        "price": 6.99,
        "category": "Fast Food",
        "stock": 60,
        "image_file": "https://images.unsplash.com/photo-1612392062422-31c37f3d8f9d?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    {
        "name": "Street Tacos (3pc)",
        "description": (
            "Three soft corn tortillas filled with seasoned grilled chicken, fresh pico de gallo, "
            "guacamole, shredded cabbage, and a squeeze of lime."
        ),
        "price": 9.99,
        "category": "Fast Food",
        "stock": 45,
        "image_file": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=400&h=300&fit=crop&auto=format",
        "is_active": True,
    },
    # ── Inactive (hidden from catalog) ──────────────────────────────────────────
    {
        "name": "Discontinued Gadget Guide 2018",
        "description": "This product is no longer available. Listed for archive purposes only.",
        "price": 9.99,
        "category": "Books",
        "stock": 0,
        "image_file": "placeholder.png",
        "is_active": False,
    },
]


def seed_products():
    from app import create_app, db
    from app.models import Product

    app = create_app()
    with app.app_context():
        Product.query.delete()
        db.session.commit()

        for data in SEED_PRODUCTS:
            db.session.add(Product(**data))

        db.session.commit()
        active = Product.query.filter_by(is_active=True).count()
        total  = Product.query.count()
        print(f"Seeded {total} products ({active} active, {total - active} inactive).")


if __name__ == "__main__":
    seed_products()
