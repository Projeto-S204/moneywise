from flask import Blueprint, render_template
from app.models import Category

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/categorias')
def categorias():
    receitas = Category.query.filter_by(type='receita').all()
    despesas = Category.query.filter_by(type='despesa').all()
    return render_template('categorias/list.html', receitas=receitas, despesas=despesas)