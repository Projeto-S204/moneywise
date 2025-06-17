from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")  # ou defina diretamente as configs

    db.init_app(app)

    # Importação local para evitar importação circular
    from app.transactions.routes import transactions
    from app.categories import categories_bp

    app.register_blueprint(transactions)
    app.register_blueprint(categories_bp)

    return app
