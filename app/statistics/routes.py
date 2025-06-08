from flask import Blueprint, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from config import Config
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.users_authentication.models import User
from collections import defaultdict

statistics = Blueprint(
    'statistics',
    __name__,
    url_prefix='/statistics',
    static_folder='static',
    template_folder='templates'
)

@statistics.route('/', methods=['GET'])
@jwt_required()
def statistics_page():
    try:
        user_id = get_jwt_identity()

        connection = Config.get_db_connection()
        cursor = connection.cursor()

        seis_meses_atras = datetime.now() - timedelta(days=180)
        data_inicio = seis_meses_atras.strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT transaction_type, amount 
            FROM transactions
            WHERE user_id = %s AND transaction_date >= %s
        """, (user_id, data_inicio))
        
        transacoes = cursor.fetchall()

        receitas = sum(float(valor) for tipo, valor in transacoes if tipo.lower() == 'income')
        despesas = sum(float(valor) for tipo, valor in transacoes if tipo.lower() == 'expense')
        total = receitas - despesas

        cursor.execute("""
            SELECT category, SUM(amount) FROM transactions
            WHERE user_id = %s AND transaction_type = 'income' AND transaction_date >= %s
            GROUP BY category
        """, (user_id, data_inicio))
        receitas_por_categoria = cursor.fetchall()

        cursor.execute("""
            SELECT category, SUM(amount) FROM transactions
            WHERE user_id = %s AND transaction_type = 'expense' AND transaction_date >= %s
            GROUP BY category
        """, (user_id, data_inicio))
        despesas_por_categoria = cursor.fetchall()

        cursor.execute("""
            SELECT 
                TO_CHAR(transaction_date, 'YYYY-MM') AS mes, 
                transaction_type, 
                SUM(amount)
            FROM transactions
            WHERE user_id = %s AND transaction_date >= %s
            GROUP BY mes, transaction_type
            ORDER BY mes ASC
        """, (user_id, data_inicio))

        saldos_mensais_raw = cursor.fetchall()

        saldos_mensais_dict = defaultdict(lambda: {'income': 0, 'expense': 0})

        for mes, tipo, valor in saldos_mensais_raw:
            saldos_mensais_dict[mes][tipo.lower()] += float(valor)

        meses = sorted(saldos_mensais_dict.keys())
        receitas_mensais = [saldos_mensais_dict[mes]['income'] for mes in meses]
        despesas_mensais = [saldos_mensais_dict[mes]['expense'] for mes in meses]
        saldos_mensais = [r - d for r, d in zip(receitas_mensais, despesas_mensais)]

        cursor.execute("""
            SELECT title, amount, category 
            FROM transactions
            WHERE user_id = %s AND transaction_type = 'expense' AND transaction_date >= %s
            ORDER BY amount DESC
            LIMIT 5
        """, (user_id, data_inicio))
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
    
    except Exception as e:
        flash("Erro ao carregar estatísticas.", category="error")
        print(f"[Statistics Error] {e}")
        return redirect(url_for("transactions.transactions_page"))