from config import Config
from .utils import convert_value

class TransactionsModal:
    
    @staticmethod
    def create_transaction_table():
        try:
            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:
                    query = """
                    CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id SERIAL PRIMARY KEY,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        title VARCHAR(255) NOT NULL,
                        amount DECIMAL(10, 2) NOT NULL,
                        category VARCHAR(255) NOT NULL,
                        payment_method VARCHAR(255) NOT NULL,
                        description TEXT,
                        transaction_date DATE,
                        transaction_hour TIME,
                        is_recurring BOOLEAN DEFAULT FALSE,
                        start_date DATE,
                        end_date DATE,
                        interval VARCHAR(255),
                        number_of_payments INTEGER,
                        transaction_type VARCHAR(255) NOT NULL
                    )
                    """
                    cursor.execute(query)
                    db_connection.commit()
        except Exception as e:
            print(f"Error {e}")


    @staticmethod
    def transaction_create(transaction_data: dict):
        try:
            query = """
            INSERT INTO transactions (
                title, 
                amount, 
                category, 
                payment_method, 
                transaction_date, 
                transaction_hour, 
                description, 
                is_recurring, 
                start_date, 
                end_date, 
                interval, 
                number_of_payments,
                transaction_type
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING transaction_id
            """

            values = {
                'title': transaction_data.get('title'),
                'amount': float(transaction_data['amount']) if transaction_data.get('amount') else None,
                'category': transaction_data.get('category'),
                'payment_method': transaction_data.get('payment_method'),
                'transaction_date': transaction_data.get('transaction_date'),
                'transaction_hour': transaction_data.get('transaction_hour'),
                'description': transaction_data.get('description'),
                'is_recurring': bool(transaction_data['is_recurring']) if 'is_recurring' in transaction_data else None,
                'start_date': transaction_data['start_date'] if transaction_data.get('start_date') else None,
                'end_date': transaction_data['end_date'] if transaction_data.get('end_date') else None,
                'interval': transaction_data['interval'] if transaction_data.get('interval') else None,
                'number_of_payments': int(transaction_data['number_of_payments']) if transaction_data.get('number_of_payments') else None,
                'transaction_type': transaction_data.get('transaction_type'),
            }

            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(query, tuple(values.values()))
                    transaction_id = cursor.fetchone()[0]
                    db_connection.commit()
                    return f"Transação {transaction_id} criada com sucesso!"

        except Exception as e:
            print(f"Erro ao criar transação: {e}")
            return f"Erro ao criar transação: {e}"


    @staticmethod
    def transactions_get_list(transactions_filters=None, transaction_id=None):
        try:
            query = """
            SELECT 
                transaction_id, 
                title, 
                amount::float, 
                category, 
                payment_method, 
                description, 
                TO_CHAR(transaction_date, 'YYYY-MM-DD') AS transaction_date,
                TO_CHAR(transaction_hour, 'HH24:MI') AS transaction_hour, 
                is_recurring, 
                TO_CHAR(start_date, 'YYYY-MM-DD') AS start_date, 
                TO_CHAR(end_date, 'YYYY-MM-DD') AS end_date, 
                interval, 
                number_of_payments, 
                transaction_type
            FROM 
                transactions
            WHERE
                1 = 1
            """
            params = []

            if transaction_id:
                query += " AND transaction_id = %s"
                params.append(transaction_id)

            if transactions_filters:
                filters_map = {
                    'search': "title LIKE %s",
                    'filter-type': "transaction_type = %s",
                    'filter-category': "category = %s",
                    'filter-start-date': "transaction_date >= %s",
                    'filter-end-date': "transaction_date <= %s",
                    'filter-min-amount': "amount >= %s",
                    'filter-max-amount': "amount <= %s",
                    'filter-payment-method': "payment_method = %s",
                }

                for key, value in filters_map.items():
                    if transactions_filters[key]:
                        query += f' AND {value}'
                        params.append(transactions_filters[key])

            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(query, params)
                    column_names = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    result = [dict(zip(column_names, row)) for row in rows]
                    return result

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def transaction_edit(transaction_data: dict):
        try:
            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:

                    update_fields, update_values = convert_value(transaction_data)

                    query = f"""
                    UPDATE transactions
                    SET {', '.join(update_fields)}
                    WHERE transaction_id = %s
                    """
                    cursor.execute(query, update_values)
                    db_connection.commit()
                    return True

        except Exception as e:
            print(f"Error: {e}")
            return f"Erro ao atualizar transação: {e}"
        
    @staticmethod
    def transaction_delete(transaction_id):
        try:
            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:
                    query = """
                    DELETE FROM transactions
                    WHERE transaction_id = %s
                    """
                    cursor.execute(query, (transaction_id,))
                    db_connection.commit()
                    
        except Exception as e:
            print(f"Error {e}")
            return f"Erro ao deletar transação: {e}"
