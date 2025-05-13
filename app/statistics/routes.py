from flask import Blueprint, render_template, session
from app.transactions.transaction_db import TransactionsModal

statistics = Blueprint(
    'statistics',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/statistics/static',
)

@statistics.route('/statistics')
def statistics_page():
    user_id = session.get('user_id')
    transactions = TransactionsModal.transactions_get_list(user_id=user_id)

    receitas = sum(t['amount'] for t in transactions if t['transaction_type'] == 'Receita')
    despesas = sum(t['amount'] for t in transactions if t['transaction_type'] == 'Despesa')
    total = receitas - despesas

    return render_template(
        'statistics.html',
        receitas=receitas,
        despesas=despesas,
        total=total
    )
