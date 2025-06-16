from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/category_felipe'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import main
    from app.categories import categories_bp

    app.register_blueprint(main)
    app.register_blueprint(categories_bp)

    with app.app_context():
        db.create_all()

    return app
