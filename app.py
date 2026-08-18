import os
from flask import Flask
from werkzeug.security import generate_password_hash
from Application.database import db
from Application.models import User


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///ecard.sqlite").replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
    app.debug = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_password = os.environ.get("ADMIN_PASSWORD")
        if admin_username and admin_password and not User.query.filter_by(type="admin").first():
            db.session.add(User(
                username=admin_username,
                email=os.environ.get("ADMIN_EMAIL", "admin@local"),
                password=generate_password_hash(admin_password),
                type="admin",
            ))
            db.session.commit()
        import Application.controllers  # noqa: F401
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
