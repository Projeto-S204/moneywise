from config import Config

db_connection = Config.get_db_connection()
query = db_connection.cursor()

class TransactionsQueries:
  def create_transaction_table():
    try:
      query.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
          transaction_id SERIAL PRIMARY KEY,
          title VARCHAR(255) NOT NULL,
          amount DECIMAL(10, 2) NOT NULL,
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
      )
      db_connection.commit()

      
    except Exception as e:
      db_connection.rollback()
      return str(e)
    

  def transactions_get_list():
    try:
      query.execute(
        """
        SELECT * FROM transactions
        """
      )
      transactions = query.fetchall()
      return transactions
    except Exception as e:
      return str(e)
