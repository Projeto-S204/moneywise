from flask import Blueprint, render_template
from app.models import Category

main = Blueprint('main', __name__)

@main.route('/')
def transaction_form_page():
    # Categorias fixas são aquelas com fixed=True
    categorias_estaticas = Category.query.filter_by(fixed=True).all()

    # Categorias dinâmicas são as criadas pelo usuário
    categorias_dinamicas = Category.query.filter_by(fixed=False).all()

    return render_template(
        'transaction_form_page.html',
        categorias_estaticas=categorias_estaticas,
        categorias_dinamicas=categorias_dinamicas
    )
