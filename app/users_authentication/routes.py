from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import logout_user, current_user, login_required
from datetime import datetime

from app.users_authentication.services.signin_form import UserSigninForm
from app.users_authentication.services.signup_form import UserSignupForm
from app.users_authentication.services.form_validations import (
    validate_form_on_signup,
    validade_form_on_signin,
)
from app.users_authentication.models import User

users = Blueprint(
    'users',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/users/static',
)


# Rota de login
@users.route("/signin", methods=["GET", "POST"])
def signin_page():
    form = UserSigninForm()
    if validade_form_on_signin(form):
        return redirect(url_for("transactions.transactions_page"))
    return render_template("signin_page.html", form=form)


# Rota de cadastro
@users.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = UserSignupForm()
    if validate_form_on_signup(form):
        flash("Conta criada com sucesso! Agora faça login.", "success")
        return redirect(url_for("users.signin_page"))
    return render_template("signup_page.html", form=form)


# Rota de logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home.home_page'))


# Rota de exibição do perfil
@users.route("/profile", methods=["GET"])
@login_required
def profile_page():
    return render_template("profile.html", user=current_user)


# Rota de atualização do perfil
@users.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    from app import db  # Importa o db dentro da função para evitar circular import
    try:
        data = request.json
        current_user.name = data.get('name')
        current_user.email = data.get('email')

        birthday_str = data.get('birthday')
        if birthday_str:
            try:
                current_user.birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

        db.session.commit()
        return jsonify({'success': True, 'message': 'Dados atualizados com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro ao atualizar perfil.'}), 500

@users.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    from app import db  # Importa o db dentro da função para evitar circular import
    try:
        # Deleta a conta do usuário
        db.session.delete(current_user)
        db.session.commit()

        # Faz o logout após a exclusão
        logout_user()

        return jsonify({'success': True, 'message': 'Conta deletada com sucesso.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro ao deletar conta.'}), 500