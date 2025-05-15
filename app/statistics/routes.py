from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from config import Config

statistics = Blueprint(
    'statistics',
    __name__,
    url_prefix='/statistics',
    static_folder='static',
    template_folder='templates'
)

@statistics.route('/', methods=['GET'])
@login_required
def statistics_page():
    connection = Config.get_db_connection()
    cursor = connection.cursor()

    seis_meses_atras = datetime.now() - timedelta(days=180)
    data_inicio = seis_meses_atras.strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT transaction_type, amount 
        FROM transactions
        WHERE user_id = %s AND transaction_date >= %s
    """, (current_user.id, data_inicio))
    
    transacoes = cursor.fetchall()

    receitas = sum(float(valor) for tipo, valor in transacoes if tipo.lower() == 'income')
    despesas = sum(float(valor) for tipo, valor in transacoes if tipo.lower() == 'expense')
    total = receitas - despesas

    cursor.execute("""
        SELECT category, SUM(amount) FROM transactions
        WHERE user_id = %s AND transaction_type = 'income' AND transaction_date >= %s
        GROUP BY category
    """, (current_user.id, data_inicio))
    receitas_por_categoria = cursor.fetchall()

    cursor.execute("""
        SELECT category, SUM(amount) FROM transactions
        WHERE user_id = %s AND transaction_type = 'expense' AND transaction_date >= %s
        GROUP BY category
    """, (current_user.id, data_inicio))
    despesas_por_categoria = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "statistics.html",
        receitas=receitas,
        despesas=despesas,
        total=total,
        receitas_por_categoria=receitas_por_categoria,
        despesas_por_categoria=despesas_por_categoria
    )