from flask import Blueprint

categories_bp = Blueprint('categories', __name__, template_folder='templates')

from app.categories import routes  # importa as rotas ao registrar o blueprint
