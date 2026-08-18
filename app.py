from flask import Flask
from Application.database import db
app=None

def create_app():
    # global app
    app=Flask(__name__)
    app.config["SECRET_KEY"] = __import__("os").environ.get("SECRET_KEY", "dev-only-change-me")
    app.config["SECRET_KEY"] = __import__("os").environ.get("SECRET_KEY", "dev-only-change-me")
    app.debug=False
    app.config["SQLALCHEMY_DATABASE_URI"] = __import__("os").environ.get("DATABASE_URL", "sqlite:///ecard.sqlite")
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://", 1) #step 3 Database
    db.init_app(app) #step 3 Database
    with app.app_context():
        import Application.controllers
    # with app.app_context():
    #     pass
    return app

app=create_app()
# with app.app_context():
    #from Application.controllers import * #step2 controllers
# from Application.models import * # making connection with models module using controllers so no need for this

if __name__ == "__main__":
    app.run()
