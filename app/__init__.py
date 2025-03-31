from flask import Flask
from .home.routes import home
from .transactions.routes import transactions
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()

from app.users_authentication.routes import user_bp  # noqa: E402


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(home)
    app.register_blueprint(transactions)
    app.register_blueprint(user_bp)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    return app
