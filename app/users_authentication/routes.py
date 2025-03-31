from flask import Blueprint, render_template, redirect, url_for
from app.users_authentication.services.signin_form import UserSigninForm
from app.users_authentication.services.signup_form import UserSignupForm
from app.users_authentication.services.form_validations import (
    validate_form_on_signup,
    validade_form_on_signin,
)
# from app.users_authentication.utils import TokenManager
from flask_login import logout_user
from flask import flash
from app.users_authentication.models import User


user_bp = Blueprint(
    'users',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='',
)


@user_bp.route('/users')
def show_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("show_users.html", users=users)


@user_bp.route('/iniciar')
def iniciar():
    return render_template("iniciar.html")


@user_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.iniciar'))


@user_bp.route("/user-signin", methods=["GET", "POST"])
def customer_signin_page():
    form = UserSigninForm()
    if validade_form_on_signin(form):
        return redirect(url_for("users.iniciar"))
    return render_template("user_signin_page.html", form=form)


@user_bp.route("/user-signup", methods=["GET", "POST"])
def customer_signup_page():
    form = UserSignupForm()
    print("Chamando validate_form_on_signup")
    if validate_form_on_signup(form):
        flash("Conta criada com sucesso! Agora faça login.", "success")
        return redirect(url_for("users.customer_signin_page"))
    return render_template("user_signup_page.html", form=form)
