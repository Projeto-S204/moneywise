from config import Config

class TransactionsQueries:
    
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
                        type VARCHAR(255) NOT NULL,
                        category VARCHAR(255),
                        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        description TEXT,
                        is_recurring BOOLEAN DEFAULT FALSE,
                        start_date DATE,
                        end_date DATE,
                        interval INTEGER,
                        payment_method VARCHAR(255),
                        number_of_payments INTEGER
                    )
                    """
                    cursor.execute(query)
                    db_connection.commit()

        except Exception as e:
            if db_connection:
                db_connection.rollback()
            return str(e)

    @staticmethod
    def transactions_get_list(
        type=None, 
        category=None,
        start_date=None, 
        end_date=None,
        min_amount=None,
        max_amount=None, 
        payment_method=None
    ):
        try:
            query = """
            SELECT 
              *
            FROM
              transactions
            WHERE
              (%s IS NULL OR type IS NULL OR type = %s)
              AND (%s IS NULL OR category IS NULL OR category = %s)
              AND (%s IS NULL OR start_date IS NULL OR start_date >= %s)
              AND (%s IS NULL OR end_date IS NULL OR end_date <= %s)
              AND (%s IS NULL OR amount >= %s)
              AND (%s IS NULL OR amount <= %s)
              AND (%s IS NULL OR payment_method IS NULL OR payment_method = %s)
            """
            
            with Config.get_db_connection() as db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(query, (
                        type, type, 
                        category, category, 
                        start_date, start_date, 
                        end_date, end_date, 
                        min_amount, min_amount, 
                        max_amount, max_amount, 
                        payment_method, payment_method
                    ))
                    
                    return cursor.fetchall()

        except Exception as e:
            return str(e)