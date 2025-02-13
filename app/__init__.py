from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .home.routes import home
from config import Config

db = SQLAlchemy()

# Preciso ajustar esse import dentro da função!


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.users_authentication.routes import users_authentication
    app.register_blueprint(users_authentication)
    app.register_blueprint(home)

    db.init_app(app)

    return app
