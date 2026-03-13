import os
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # Use /tmp on Vercel (serverless), otherwise use instance folder
    if os.environ.get("VERCEL"):
        db_path = "/tmp/store.db"
    else:
        os.makedirs(app.instance_path, exist_ok=True)
        db_path = os.path.join(app.instance_path, "store.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", f"sqlite:///{db_path}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Override config for testing
    if test_config is not None:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from .routes.catalog import catalog_bp
    from .routes.cart import cart_bp
    app.register_blueprint(catalog_bp)
    app.register_blueprint(cart_bp)

    # Context processor: cart_count available in all templates
    @app.context_processor
    def inject_cart_count():
        cart = session.get("cart", {})
        count = sum(item["quantity"] for item in cart.values())
        return {"cart_count": count}

    # Register error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    return app
