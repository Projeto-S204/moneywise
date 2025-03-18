from flask import Blueprint, redirect, render_template, request, url_for, flash
from .transaction_db import TransactionsModal

TransactionsModal.create_transaction_table()

transactions = Blueprint(
    'transactions',
    __name__,
    url_prefix='/transactions',
    static_folder='static',
    template_folder='templates'
)


@transactions.route('/', methods=['GET'])
def transactions_page():
    transactions_filters = {key: request.args.get(key) for key in [
        'search', 'filter-type', 'filter-category', 'filter-start-date',
        'filter-end-date', 'filter-min-amount', 'filter-max-amount',
        'filter-payment-method'
    ]}

    transactions_list = TransactionsModal.transactions_get_list(
        transactions_filters
    )
    return render_template('transactions_list_page.html',
                           transactions=transactions_list,
                           transactions_filters=transactions_filters)


@transactions.route('/create', methods=['GET', 'POST'])
def transaction_create_page():

    if request.method == 'POST':
        try:
            transaction_data = {key: request.form.get(key) for key in [
                'title', 'amount', 'category', 'payment_method', 'description',
                'transaction_date', 'transaction_hour', 'is_recurring',
                'start_date',
                'end_date', 'interval', 'number_of_payments',
                'transaction_type']
            }

            TransactionsModal.transaction_create(transaction_data)

            flash('Criada com sucesso.', 'success')
            return redirect(url_for('transactions.transactions_page'))
        except Exception as e:
            flash('Ocorreu um erro ao criar, tente novamente.', 'error')
            print(f"Error: {e}")
    return render_template('transaction_form_page.html', transaction=None)


@transactions.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def transaction_edit_page(transaction_id):

    if request.method == 'GET':
        transaction = TransactionsModal.transactions_get_list(
            transaction_id=transaction_id
        )[0]
        print(transaction_id)
        print(transaction)

    if request.method == 'POST':
        try:
            transaction_data = {key: request.form.get(key) for key in [
                'title', 'amount', 'category', 'payment_method', 'description',
                'transaction_date', 'transaction_hour', 'is_recurring',
                'start_date', 'end_date', 'interval', 'number_of_payments',
                'transaction_type']
            }
            transaction_data['transaction_id'] = transaction_id

            TransactionsModal.transaction_edit(transaction_data)

            flash('Editado com sucesso.', 'success')
            return redirect(url_for('transactions.transactions_page'))
        except Exception as e:
            flash('Ocorreu um erro ao editar, tente novamente.', 'error')
            print(f"Error: {e}")
            return render_template(
                'transaction_form_page.html', transaction=transaction
            )


@transactions.route('/delete/<int:transaction_id>', methods=['GET'])
def transaction_delete(transaction_id):
    try:
        TransactionsModal.transaction_delete(transaction_id)
        flash('Deletado com sucesso.', 'success')
    except Exception as e:
        flash('Ocorreu um erro ao deletar', 'error')
        print(f"Error: {e}")

    return redirect(url_for('transactions.transactions_page'))
