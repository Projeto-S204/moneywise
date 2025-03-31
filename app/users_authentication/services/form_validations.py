from flask import flash
from app.users_authentication.models import User
from flask_login import login_user
from config import db
# from app.users_authentication.utils import TokenManager


def validade_form_on_signin(form):

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            email=form.email.data).first()
        if attempted_user and attempted_user.check_password(
                form.password.data):
            login_user(attempted_user)
            flash(f"Login bem-sucedido! Bem-vindo, {attempted_user.name}",
                  category="success")
            # token = TokenManager.generate_token(attempted_user.id)
            return True

        flash("Credenciais inválidas! Tente novamente.", category="danger")
        return False


def validate_form_on_signup(form):

    if form.validate_on_submit():
        user_to_create = User(
            email=form.email_address.data,
            name=form.username.data,
            password=form.password.data,
            birthday=form.birthday.data,
            # avatar=form.avatar.data
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        # token = TokenManager.generate_token(user_to_create.id)
        return True

    if form.errors:
        for err_msg in form.errors.values():
            flash(f"Ocorreu um erro ao criar a conta: {err_msg}",
                  category="danger")
            print(f"Flash: Erro ao criar conta: {err_msg}")
    return False
