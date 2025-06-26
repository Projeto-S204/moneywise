from flask import render_template, request, redirect, url_for
from app.categories import categories_bp
from app.__init__ import db
from app.categories.models import Category

@categories_bp.route('/categorias')
def listar_categorias():
    receitas = Category.query.filter_by(type='receita').all()
    despesas = Category.query.filter_by(type='despesa').all()
    return render_template('categories/categorias_list.html', receitas=receitas, despesas=despesas)

@categories_bp.route('/categorias/nova', methods=['GET', 'POST'])
def nova_categoria():
    if request.method == 'POST':
        nome = request.form['name']
        tipo = request.form['type']
        nova = Category(name=nome, type=tipo)
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for('categories.listar_categorias'))
    return render_template('categories/categorias_new.html')

@categories_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):
    categoria = Category.query.get_or_404(id)
    if request.method == 'POST':
        categoria.name = request.form['name']
        categoria.type = request.form['type']
        db.session.commit()
        return redirect(url_for('categories.listar_categorias'))
    return render_template('categories/categorias_edit.html', categoria=categoria)

@categories_bp.route('/categorias/deletar/<int:id>', methods=['POST'])
def deletar_categoria(id):
    categoria = Category.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categories.listar_categorias'))
