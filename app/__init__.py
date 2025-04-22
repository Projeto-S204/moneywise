from flask import Flask
from .home.routes import home
from .transactions.routes import transactions
from app.users_authentication.routes import users
from config import Config, db, login_manager, jwt, migrate, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(home)
    app.register_blueprint(transactions)
    app.register_blueprint(users)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from app.users_authentication.models import User  # <-- Importa aqui!

    return app
