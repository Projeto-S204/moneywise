from flask import Flask
from .home.routes import home
from .transactions.routes import transactions
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(home)
    app.register_blueprint(transactions)

    return app