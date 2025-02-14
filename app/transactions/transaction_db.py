from config import Config

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
            print(f"Erro ao criar a tabela: {e}")
        

    @staticmethod
    def transaction_create(transaction_data: dict):
        try:
            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:

                    query = """
                    INSERT INTO transactions (
                        title, amount, category, payment_method, 
                        transaction_date, transaction_hour, description, is_recurring, 
                        start_date, end_date, interval, number_of_payments, transaction_type
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING transaction_id
                    """

                    cursor.execute(query, (
                        transaction_data['title'],
                        float(transaction_data['amount']) if transaction_data.get('amount') else None,
                        transaction_data['category'],
                        transaction_data['payment_method'],
                        transaction_data['transaction_date'] if transaction_data.get('transaction_date') else None,
                        transaction_data['transaction_hour']if transaction_data.get('transaction_hour') else None,
                        transaction_data['description'] if transaction_data.get('description') else None,
                        bool(transaction_data['is_recurring']) if transaction_data.get('is_recurring') is not None else None,
                        transaction_data['start_date'] if transaction_data.get('start_date') else None,
                        transaction_data['end_date'] if transaction_data.get('end_date') else None,
                        transaction_data['interval'] if transaction_data.get('interval') else None,
                        int(transaction_data['number_of_payments']) if transaction_data.get('number_of_payments') else None,
                        transaction_data['transaction_type']
                    ))

                    transaction_id = cursor.fetchone()[0]
                    db_connection.commit()
                    return f"Transação {transaction_id} criada com sucesso!"
        except Exception as e:
            print(e)
            return f"Erro ao criar transação: {e}"

    @staticmethod
    def transactions_get_list(transaction_id=None, amount_min=None, amount_max=None, date_start=None, date_end=None, category=None, transaction_type=None, payment_method=None, is_recurring=None):
        try:
            query = """
            SELECT 
                * 
            FROM 
                transactions
            WHERE
                1 = 1
            """
            params = []

            if transaction_id is not None:
                query += " AND transaction_id = %s"
                params.append(transaction_id)
            if amount_min is not None:
                query += " AND amount >= %s"
                params.append(amount_min)
            if amount_max is not None:
                query += " AND amount <= %s"
                params.append(amount_max)
            if date_start is not None:
                query += " AND transaction_date >= %s"
                params.append(date_start)
            if date_end is not None:
                query += " AND transaction_date <= %s"
                params.append(date_end)
            if category is not None:
                query += " AND category = %s"
                params.append(category)
            if transaction_type is not None:
                query += " AND transaction_type = %s"
                params.append(transaction_type)
            if payment_method is not None:
                query += " AND payment_method = %s"
                params.append(payment_method)
            if is_recurring is not None:
                query += " AND is_recurring = %s"
                params.append(is_recurring)

            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchall()

        except Exception as e:
            print(e)
            return str(e)

    @staticmethod
    def transaction_edit(transaction_data: dict):
        try:
            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:
                    update_fields = []
                    update_values = []

                    for key, value in transaction_data.items():
                        if key != "transaction_id":
                            if key in ["start_date", "end_date"] and value == "":
                                value = None 
                            if key in ['is_recurring'] and value == None:
                                value = False
                                transaction_data['start_date'] = None
                                transaction_data['end_date'] = None
                                transaction_data['interval'] = None
                                transaction_data['number_of_payments'] = None

                            update_fields.append(f"{key} = %s")
                            update_values.append(value)

                    if not update_fields:
                        return "Nenhuma atualização fornecida."

                    set_clause = ", ".join(update_fields)
                    update_values.append(transaction_data['transaction_id'])

                    for i in range(len(update_fields)):
                        print(f"{update_fields[i]} = {update_values[i]}")

                    query = f"""
                    UPDATE transactions
                    SET {set_clause}
                    WHERE transaction_id = %s
                    RETURNING transaction_id
                    """

                    cursor.execute(query, update_values)
                    db_connection.commit()

        except Exception as e:
            print(e)
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
            print(e)
            return f"Erro ao deletar transação: {e}"
        