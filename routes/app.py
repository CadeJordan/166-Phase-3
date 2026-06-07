from datetime import datetime
import os

from flask import Flask, render_template, session

import config
from data import queries
from routes import admin_bp, auth_bp, buyer_bp, public_bp, seller_bp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(ROOT, "templates"),
        static_folder=os.path.join(ROOT, "routes", "static"),
    )
    app.config.from_object(config)

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        return {
            "current_user_login": session.get("demo_user"),
            "current_user_role": session.get("demo_role"),
        }

    @app.template_filter("currency")
    def currency_filter(value):
        return f"${value:,.2f}"

    @app.template_filter("datetime_fmt")
    def datetime_fmt(value):
        if isinstance(value, datetime):
            return value.strftime("%b %d, %Y %I:%M %p")
        return value

    @app.errorhandler(404)
    def not_found(e):
        return render_template("pages/errors/404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
