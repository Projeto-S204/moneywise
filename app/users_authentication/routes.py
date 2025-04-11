from flask import Blueprint, render_template, redirect, url_for
from app.users_authentication.services.signin_form import UserSigninForm
from app.users_authentication.services.signup_form import UserSignupForm
from app.users_authentication.services.form_validations import (
    validate_form_on_signup,
    validade_form_on_signin,
)
# from app.users_authentication.utils import TokenManager
from flask_login import logout_user, current_user
from flask import flash
from app.users_authentication.models import User


users = Blueprint(
    'users',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='',
)


@users.route("/signin", methods=["GET", "POST"])
def signin_page():
    form = UserSigninForm()
    if validade_form_on_signin(form):
        return redirect(url_for("transactions.transactions_page"))
    return render_template("signin_page.html", form=form)

@users.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = UserSignupForm()

    if validate_form_on_signup(form):
        flash("Conta criada com sucesso! Agora faça login.", "success")
        return redirect(url_for("users.signin_page"))
    return render_template("signup_page.html", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home.home_page'))