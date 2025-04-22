from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    from app.transactions.routes import transactions_bp
    from app.category_crud.routes import category_bp

    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(category_bp, url_prefix='/categories')

    return app
