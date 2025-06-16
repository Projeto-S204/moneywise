from config import db
from flask import flash, url_for
from app.users_authentication.models import User
from flask_mail import Message
from config import mail
from urllib.parse import quote
from app.users_authentication.utils.token import (
    generate_reset_token,
    confirm_reset_token,
)
from app.users_authentication.services.reset_password_form \
    import ResetPasswordForm

from urllib.parse import unquote
from flask import redirect, render_template


def delete_user_logic(user, password):
    if user.check_password(password):
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"[ERRO] Falha ao deletar usuário: {e}")


def send_reset_email(user, token):
    safe_token = quote(token)

    reset_url = url_for(
        "users.reset_password", token=safe_token, _external=True
    )

    msg = Message(
        subject="Recuperação de senha - MoneyWise",
        recipients=[user.email],
        html=f"""
        <p>Olá, {user.name}!</p>
        <p>Para redefinir sua senha, clique no botão abaixo:</p>
        <p>
            <a href="{reset_url}"
               style="display: inline-block;
                      background-color: #efa23b;
                      color: #1f1f23;
                      text-decoration: none;
                      font-weight: bold;
                      padding: 12px 20px;
                      border-radius: 6px;
                      font-family: 'Segoe UI', Tahoma, sans-serif;
                      font-size: 16px;
                      transition: background-color 0.3s ease;">
                Redefinir Senha
            </a>
        </p>
        <p>Se você não solicitou isso,
           entre em contato com o suporte MoneyWise.</p>
        <p>Atenciosamente,<br>Equipe MoneyWise</p>
        """
    )

    mail.send(msg)


def process_reset_request(form):
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_reset_token(user.email)
            send_reset_email(user, token)
            return True
        else:
            flash("E-mail não cadastrado.", "danger")
            return False
    return False


def reset_user_password(user, new_password):
    user.set_password(new_password)
    db.session.commit()


def reset_password_logic(token, form_class=ResetPasswordForm):
    token = unquote(token)
    email = confirm_reset_token(token)
    if not email:
        flash("Link inválido ou expirado.", category="danger")
        return redirect(url_for("users.forgot_password_page"))

    form = form_class()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            reset_user_password(user, form.password.data)
            flash("Senha redefinida com sucesso!", category="success")
            return redirect(url_for("users.signin_page"))
        else:
            flash("Usuário não encontrado.", category="danger")

    return render_template("reset_password_page.html", form=form)
