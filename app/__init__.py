from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager

from .home.routes import home
from .transactions.routes import transactions

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()


from app.users_authentication.routes import user_bp  # noqa: E402


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(user_bp)
    app.register_blueprint(home)
    app.register_blueprint(transactions)
    return app
