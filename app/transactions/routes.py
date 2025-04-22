from flask import request, jsonify, render_template
from app import db
from app.transactions.transaction_db import Transaction
from app.category_crud.models import Category
from datetime import datetime
from app.category_crud.models import Category
from flask import Blueprint

transactions_bp = Blueprint('transactions', __name__, template_folder='templates')

@transactions_bp.route('/transactions/new')
def transaction_form():
    categories = Category.query.all()
    return render_template('transaction_form_page.html', categories=categories)

def create_transaction():
    data = request.get_json()

    category = Category.query.get(data.get('category_id'))
    if not category:
        return jsonify({"error": "Invalid category"}), 400

    new_transaction = Transaction(
        amount=data['amount'],
        description=data.get('description'),
        date=datetime.strptime(data['date'], "%Y-%m-%d"),
        category_id=category.id
    )

    try:
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify(new_transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
