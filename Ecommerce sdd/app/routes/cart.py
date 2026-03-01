from decimal import Decimal
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, abort,
)
from ..models import Product
from .. import db

cart_bp = Blueprint("cart", __name__)


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_cart():
    """Return the cart dict from the session (default empty)."""
    return session.get("cart", {})


def save_cart(cart):
    """Persist cart dict back to the session."""
    session["cart"] = cart
    session.modified = True


# ── Routes ───────────────────────────────────────────────────────────────────

@cart_bp.route("/cart")
def index():
    """GET /cart — display cart contents."""
    cart = get_cart()
    cart_items = []
    product_warnings = []

    for key, item in cart.items():
        product = db.session.get(Product, item["product_id"])
        line = dict(item)
        line["line_total"] = Decimal(item["price"]) * item["quantity"]

        if product is None or not product.is_active:
            line["warning"] = "This product is no longer available."
            product_warnings.append(line)
        else:
            if product.stock == 0:
                line["warning"] = "Currently out of stock."
                product_warnings.append(line)
            cart_items.append(line)

    subtotal = sum(Decimal(i["price"]) * i["quantity"] for i in cart.values())
    return render_template(
        "cart/index.html",
        cart_items=cart_items,
        subtotal=subtotal,
        product_warnings=product_warnings,
    )


@cart_bp.route("/cart/add", methods=["POST"])
def add():
    """POST /cart/add — add a product to the cart."""
    try:
        product_id = int(request.form["product_id"])
        quantity = int(request.form.get("quantity", 1))
    except (KeyError, ValueError):
        abort(400)

    product = db.get_or_404(Product, product_id)

    if not product.is_active:
        abort(404)

    if product.stock == 0:
        flash("Sorry, this item is out of stock.", "danger")
        return redirect(url_for("catalog.detail", id=product_id))

    cart = get_cart()
    key = str(product_id)

    if key in cart:
        cart[key]["quantity"] += quantity
    else:
        cart[key] = {
            "product_id": product_id,
            "name": product.name,
            "price": str(product.price),
            "quantity": quantity,
            "image_file": product.image_file,
        }

    # Cap at available stock
    if cart[key]["quantity"] > product.stock:
        cart[key]["quantity"] = product.stock
        flash(f"Only {product.stock} available — quantity adjusted.", "warning")
    else:
        flash("Added to cart!", "success")

    save_cart(cart)
    return redirect(url_for("cart.index"))


@cart_bp.route("/cart/update", methods=["POST"])
def update():
    """POST /cart/update — change quantity of a cart item."""
    try:
        product_id = int(request.form["product_id"])
        quantity = int(request.form["quantity"])
    except (KeyError, ValueError):
        return redirect(url_for("cart.index"))

    cart = get_cart()
    key = str(product_id)

    if key not in cart:
        return redirect(url_for("cart.index"))

    if quantity <= 0:
        cart.pop(key)
        flash("Item removed from cart.", "info")
    else:
        product = db.session.get(Product, product_id)
        if product and product.stock > 0:
            capped = min(quantity, product.stock)
            if capped < quantity:
                flash(f"Only {product.stock} available — quantity adjusted.", "warning")
            cart[key]["quantity"] = capped
        else:
            cart[key]["quantity"] = quantity

    save_cart(cart)
    return redirect(url_for("cart.index"))


@cart_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove(product_id):
    """POST /cart/remove/<id> — remove item from cart."""
    cart = get_cart()
    cart.pop(str(product_id), None)
    save_cart(cart)
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart.index"))
