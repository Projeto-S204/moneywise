from flask import Blueprint, render_template
from .transaction_db import TransactionsQueries

transactions_db = TransactionsQueries
transactions_db.create_transaction_table()

transactions = Blueprint(
    'transactions',
    __name__,
    static_url_path='',
    static_folder='static',
    template_folder='templates'
    )

@transactions.route('/transactions', methods=['GET'])
def transactions_page():
    transactions = transactions_db.transactions_get_list()
    return render_template('transactions_page.html', transactions=transactions)
