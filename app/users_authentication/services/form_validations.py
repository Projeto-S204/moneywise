from flask import flash
from app.users_authentication.models import User
from flask_login import login_user
from config import db


def validade_form_on_signin(form):

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            email=form.email.data).first()
        if attempted_user and attempted_user.check_password(
                form.password.data):
            login_user(attempted_user)
            return attempted_user
        else:
            flash("Email ou senha inválidos", category="danger")
            print("Flash: Email ou senha inválidos")

        return False


def validate_form_on_signup(form):

    if form.validate_on_submit():
        try:
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
            flash("Conta criada com sucesso!", category="success")
            return user_to_create

        except Exception as e:
            db.session.rollback()
            flash("Erro ao criar conta. Tente novamente.", category="danger")
            print(f"Flash: Erro ao criar conta: {e}")
            return False

    if form.errors:
        for err_msg in form.errors.values():
            flash(f"Ocorreu um erro ao criar a conta: {err_msg}",
                  category="danger")
            print(f"Flash: Erro ao criar conta: {err_msg}")
    return False
