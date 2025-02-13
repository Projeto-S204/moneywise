from flask import Blueprint, render_template, request
from .transaction_db import TransactionsQueries


TransactionsQueries.create_transaction_table()

transactions = Blueprint(
    'transactions',
    __name__,
    url_prefix='/transactions',
    static_url_path='',
    static_folder='static',
    template_folder='templates'
    )

@transactions.route('/', methods=['GET'])
def transactions_page():
    # type_filter = request.args.get('type', None)
    # category_filter = request.args.get('category', None)
    # start_date_filter = request.args.get('start_date', None)
    # end_date_filter = request.args.get('end_date', None)
    # min_amount_filter = request.args.get('min_amount', None)
    # max_amount_filter = request.args.get('max_amount', None)
    # payment_method_filter = request.args.get('payment_method', None)

    # transactions = TransactionsQueries.transactions_get_list(
    #     type=type_filter,
    #     category=category_filter,
    #     start_date=start_date_filter,
    #     end_date=end_date_filter,
    #     min_amount=min_amount_filter,
    #     max_amount=max_amount_filter,
    #     payment_method=payment_method_filter
    # )

    return render_template('transactions_list_page.html')

@transactions.route('/create', methods=['GET', 'POST'])
def transaction_create_page():
    return render_template('transaction_form_page.html')
