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
    transactions_list = TransactionsModal.transactions_get_list()
    return render_template('transactions_list_page.html', transactions=transactions_list)

@transactions.route('/create', methods=['GET', 'POST'])
def transaction_create_page():
    if request.method == 'POST':
        try:
            transaction_data = {key: request.form.get(key) for key in [
                'title', 'amount', 'category', 'payment_method', 'description', 
                'transaction_date', 'transaction_hour', 'is_recurring', 'start_date',
                'end_date', 'interval', 'number_of_payments', 'transaction_type']
            }

            TransactionsModal.transaction_create(transaction_data)
            flash('Transação criada com sucesso!', 'success')
            return redirect(url_for('transactions.transactions_page'))
        except Exception as e:
            flash(f'Erro ao criar transação: {str(e)}', 'danger')
    
    return render_template('transaction_form_page.html', transaction=None)

@transactions.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def transaction_edit_page(transaction_id):
    transaction = TransactionsModal.transactions_get_list(transaction_id)
    
    if request.method == 'POST':
        try:
            transaction_data = {key: request.form.get(key) for key in [
                'title', 'amount', 'category', 'payment_method', 'description', 
                'transaction_date','transaction_hour', 'is_recurring', 
                'start_date', 'end_date', 'interval', 'number_of_payments', 'transaction_type']
            }
            transaction_data['transaction_id'] = transaction_id
            
            TransactionsModal.transaction_edit(transaction_data)
            flash('Transação atualizada com sucesso!', 'success')
            return redirect(url_for('transactions.transactions_page'))
        except Exception as e:
            flash(f'Erro ao atualizar transação: {str(e)}', 'danger')
    
    return render_template('transaction_form_page.html', transaction=transaction)


@transactions.route('/delete/<int:transaction_id>', methods=['GET'])
def transaction_delete(transaction_id):
    try:
        TransactionsModal.transaction_delete(transaction_id)
        flash('Transação deletada com sucesso!', 'success')
    except Exception as e:
        print(e)
        flash(f'Erro ao deletar transação: {str(e)}', 'danger')

    return redirect(url_for('transactions.transactions_page'))