from flask import flash
from app.users_authentication.models import User
from flask_login import login_user  # current_user
from config import db


def validade_form_on_signin(form):

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if (
            attempted_user
            and attempted_user.check_password(form.password.data)
        ):
            login_user(attempted_user)
            return attempted_user
        else:
            flash("Email ou senha inválidos", category="danger")
            print("Flash: Email ou senha inválidos")

        return False


def validate_form_on_signup(form):
    if not form.validate_on_submit():
        for err_msgs in form.errors.values():
            for msg in err_msgs:
                flash(msg, category="danger")
                print(f"Flash: Erro ao criar conta: {msg}")
        return False

    try:
        user_to_create = User(
            email=form.email_address.data,
            name=form.username.data,
            password=form.password.data,
            birthday=form.birthday.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        return user_to_create

    except Exception as e:
        db.session.rollback()
        flash("Erro ao criar conta. Tente novamente.", category="danger")
        print(f"Flash: Erro ao criar conta: {e}")
        return False
