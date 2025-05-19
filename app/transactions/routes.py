from flask import Blueprint, redirect, render_template, request, url_for, flash
from app.users_authentication.models import User
from .transaction_db import TransactionsModal
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity,
    jwt_required
)


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
    try:
        verify_jwt_in_request()
    except Exception:
        flash(
            "Sessão expirada. Faça login novamente.",
            category="token_expired"
        )
        return redirect(url_for("users.signin_page"))

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    transactions_filters = {key: request.args.get(key) for key in [
        'search', 'filter-type', 'filter-category', 'filter-start-date',
        'filter-end-date', 'filter-min-amount', 'filter-max-amount',
        'filter-payment-method']
    }

    category_colors = {
        'Casa': '#F7B7B7',
        'Viagem': '#B2D7F6',
        'Entretenimento': '#F1D7A7',
        'Estudos': '#B7D6B5',
        'Saúde': '#F5D1D1',
        'Mercado': '#D0E5D7'
    }

    transactions_list = TransactionsModal.transactions_get_list(
        transactions_filters, user_id=user_id
    )
    return render_template(
        'transactions_list_page.html',
        user=user,
        transactions=transactions_list,
        transactions_filters=transactions_filters,
        category_colors=category_colors
    )


@transactions.route('/create', methods=['GET', 'POST'])
@jwt_required()
def transaction_create_page():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        try:
            transaction_data = {key: request.form.get(key) for key in [
                'title', 'amount', 'category', 'payment_method', 'description',
                'transaction_date', 'transaction_hour', 'is_recurring',
                'start_date',
                'end_date', 'interval', 'number_of_payments',
                'transaction_type']
            }

            TransactionsModal.transaction_create(
                transaction_data, user_id=user_id
            )

            flash('Criada com sucesso.', category='success')
            return redirect(url_for('transactions.transactions_page'))
        except Exception as e:
            flash(
                'Ocorreu um erro ao criar, tente novamente.',
                category='error'
            )
            print(f"Error: {e}")

    return render_template('transaction_form_page.html', transaction=None)


@transactions.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def transaction_edit_page(transaction_id):

    try:
        verify_jwt_in_request()
    except Exception:
        return redirect(url_for("users.signin_page"))

    if request.method == 'GET':
        transaction = TransactionsModal.transactions_get_list(
            transaction_id=transaction_id
        )[0]

    if request.method == 'POST':
        try:
            transaction_data = {key: request.form.get(key) for key in [
                'title', 'amount', 'category', 'payment_method', 'description',
                'start_date', 'end_date', 'interval',
                'number_of_payments', 'transaction_type']
            }
            transaction_data['transaction_id'] = transaction_id

            TransactionsModal.transaction_edit(transaction_data)
            return redirect(url_for('transactions.transactions_page'))
        except Exception as e:
            flash(
                'Ocorreu um erro ao editar, tente novamente.',
                category='error'
            )
            print(f"Error: {e}")

    return render_template(
        'transaction_form_page.html',
        transaction=transaction
    )


@transactions.route('/delete/<int:transaction_id>', methods=['GET'])
def transaction_delete(transaction_id):

    try:
        verify_jwt_in_request()
    except Exception:
        return redirect(url_for("users.signin_page"))

    try:
        TransactionsModal.transaction_delete(transaction_id)
    except Exception as e:
        flash('Ocorreu um erro ao deletar', category='error')
        print(f"Error: {e}")

    return redirect(url_for('transactions.transactions_page'))
