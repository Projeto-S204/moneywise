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

    # Saldo mês a mês (últimos 6 meses)
    cursor.execute("""
        SELECT 
            TO_CHAR(transaction_date, 'YYYY-MM') AS mes, 
            transaction_type, 
            SUM(amount)
        FROM transactions
        WHERE user_id = %s AND transaction_date >= %s
        GROUP BY mes, transaction_type
        ORDER BY mes ASC
    """, (current_user.id, data_inicio))


    saldos_mensais_raw = cursor.fetchall()

    # Organiza os dados no formato: {'2025-01': {'income': 1000, 'expense': 500}, ...}
    from collections import defaultdict

    saldos_mensais_dict = defaultdict(lambda: {'income': 0, 'expense': 0})

    for mes, tipo, valor in saldos_mensais_raw:
        saldos_mensais_dict[mes][tipo.lower()] += float(valor)

    # Constrói listas para plotar no gráfico
    meses = sorted(saldos_mensais_dict.keys())
    receitas_mensais = [saldos_mensais_dict[mes]['income'] for mes in meses]
    despesas_mensais = [saldos_mensais_dict[mes]['expense'] for mes in meses]
    saldos_mensais = [receitas_mensais[i] - despesas_mensais[i] for i in range(len(meses))]

    # Top 5 maiores despesas
    cursor.execute("""
        SELECT title, amount, category 
        FROM transactions
        WHERE user_id = %s AND transaction_type = 'expense' AND transaction_date >= %s
        ORDER BY amount DESC
        LIMIT 5
    """, (current_user.id, data_inicio))

    top5Despesas = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
    "statistics.html",
    receitas=receitas,
    despesas=despesas,
    total=total,
    receitas_por_categoria=receitas_por_categoria,
    despesas_por_categoria=despesas_por_categoria,
    meses=meses,
    receitas_mensais=receitas_mensais,
    despesas_mensais=despesas_mensais,
    saldos_mensais=saldos_mensais,
    top5Despesas=top5Despesas
    )
