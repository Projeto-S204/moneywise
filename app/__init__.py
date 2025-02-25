from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager

from .home.routes import home
from .transactions.routes import transactions

db = SQLAlchemy()
jwt = JWTManager()

from app.users_authentication.routes import users_authentication  # noqa:E402


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(users_authentication)
    app.register_blueprint(home)
    app.register_blueprint(transactions)
    db.init_app(app)
    jwt.init_app(app)
    return app
