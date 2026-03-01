from datetime import datetime, timezone
from . import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_file = db.Column(db.String(200), nullable=False, default="placeholder.png")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Product id={self.id} name={self.name!r}>"
