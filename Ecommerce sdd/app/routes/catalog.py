from flask import Blueprint, render_template, request, abort
from ..models import Product
from .. import db

catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.route("/")
def index():
    q        = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    query = Product.query.filter_by(is_active=True)

    if q:
        search = f"%{q}%"
        query = query.filter(
            db.or_(
                Product.name.ilike(search),
                Product.description.ilike(search),
            )
        )

    if category:
        query = query.filter(Product.category == category)

    products = query.order_by(Product.created_at.desc()).all()

    # All distinct categories for filter pills
    cat_rows = (
        db.session.query(Product.category)
        .filter_by(is_active=True)
        .distinct()
        .order_by(Product.category)
        .all()
    )
    categories = [c[0] for c in cat_rows]

    return render_template(
        "catalog/index.html",
        products=products,
        query=q,
        category=category,
        categories=categories,
    )


@catalog_bp.route("/products/<int:id>")
def detail(id):
    product = db.get_or_404(Product, id)
    if not product.is_active:
        abort(404)
    return render_template("catalog/detail.html", product=product)
