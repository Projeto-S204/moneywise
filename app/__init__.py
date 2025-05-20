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
        insert_default_categories()

    return app

def insert_default_categories():
    from app.models import Category

    categorias_padrao = [
        {"name": "Salário", "type": "receita", "icon": "💰"},
        {"name": "Aluguel de Imóveis", "type": "receita", "icon": "🏠"},
        {"name": "Vale Alimentação", "type": "receita", "icon": "🧾"},
        {"name": "Investimentos", "type": "receita", "icon": "📈"},
        {"name": "Outros", "type": "receita", "icon": "➕"},

        {"name": "Alimentação", "type": "despesa", "icon": "🍔"},
        {"name": "Transporte", "type": "despesa", "icon": "🚌"},
        {"name": "Aluguel", "type": "despesa", "icon": "🏠"},
        {"name": "Casa", "type": "despesa", "icon": "🧹"},
        {"name": "Educação", "type": "despesa", "icon": "🎓"},
    ]

    for cat in categorias_padrao:
        exists = Category.query.filter_by(name=cat["name"], type=cat["type"]).first()
        if not exists:
            nova = Category(name=cat["name"], type=cat["type"], icon=cat["icon"], fixed=True)
            db.session.add(nova)
    db.session.commit()
