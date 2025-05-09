from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify,
    flash,
    make_response,
    request
)
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
    # verify_jwt_in_request,
    get_jwt,
    # create_refresh_token,
)
from app.users_authentication.services.signin_form import UserSigninForm
from app.users_authentication.services.signup_form import UserSignupForm
from app.users_authentication.services.delete_form import UserDeleteForm
from app.users_authentication.services.user_service import delete_user_logic
from app.users_authentication.services.form_validations import (
    validate_form_on_signup,
    validade_form_on_signin,
)
from flask_login import logout_user, current_user, login_required
from datetime import datetime, timezone, timedelta
from app.email_utils import enviar_email


users = Blueprint(
    'users',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/users/static',
)


@users.route("/signin", methods=["GET", "POST"])
def signin_page():
    if current_user.is_authenticated:
        return redirect(url_for("transactions.transactions_page"))

    form = UserSigninForm()
    if form.is_submitted():
        user = validade_form_on_signin(form)
        if user:
            access_token = create_access_token(identity=str(user.id))
            print(f"[ROTA] Token com Flask-JWT-Extended: {access_token}")
            response = make_response(
                redirect(url_for("transactions.transactions_page"))
            )
            set_access_cookies(response, access_token)
            return response

    return render_template("signin_page.html", form=form)


@users.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = UserSignupForm()

    if form.is_submitted():
        user = validate_form_on_signup(form)
        if user:
            flash("Conta criada com sucesso. Faça login.", category="success")
            return redirect(url_for("users.signin_page"))

    return render_template("signup_page.html", form=form)


@users.route("/logout")
def logout():
    logout_user()
    response = make_response(redirect(url_for("users.signin_page")))
    unset_jwt_cookies(response)
    flash("Logout realizado com sucesso!", "success")
    return response


@users.route("/token/expires", methods=["GET"])
@jwt_required()
def token_expires():

    try:
        jwt_payload = get_jwt()
        exp_timestamp = jwt_payload.get('exp')

        if not exp_timestamp:
            return jsonify({
                "error": "Token não contém informação de expiração ('exp')."
            }), 400

        brasilia_tz = timezone(timedelta(hours=-3))

        now = datetime.now(timezone.utc).astimezone(brasilia_tz)
        exp = datetime.fromtimestamp(
            exp_timestamp, tz=timezone.utc
        ).astimezone(brasilia_tz)

        time_remaining = exp - now
        if time_remaining.total_seconds() < 0:
            return jsonify({"message": "Token já expirou."}), 401

        total_seconds = int(time_remaining.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        human_readable = f"{days}d {hours}h {minutes}m {seconds}s"
        if days == 0:
            human_readable = f"{hours}h {minutes}m {seconds}s"
        if hours == 0 and days == 0:
            human_readable = f"{minutes}m {seconds}s"

        return jsonify({
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": exp.strftime("%Y-%m-%d %H:%M:%S"),
            "time_remaining_seconds": total_seconds,
            "time_remaining_human": human_readable
        })

    except Exception as e:
        print(f"Erro ao verificar expiração do token: {e}")
        return jsonify({
            "error": "Erro ao processar a expiração do token."
        }), 500


@users.route("/profile")
@login_required
def profile_page():
    form = UserDeleteForm()
    return render_template("profile.html", user=current_user, form=form)


@users.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    from app import db
    try:
        data = request.json
        current_user.name = data.get('name')
        current_user.email = data.get('email')

        birthday_str = data.get('birthday')
        if birthday_str:
            try:
                current_user.birthday = datetime.strptime(
                    birthday_str, '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Formato de data inválido. Use YYYY-MM-DD.'
                }), 400

        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Dados atualizados com sucesso.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar perfil: {str(e)}'
        }), 500


@users.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    form = UserDeleteForm()
    if form.is_submitted():
        success = delete_user_logic(current_user, form.password.data)

        if success:
            logout_user()
            response = make_response(redirect(url_for("users.signin_page")))
            unset_jwt_cookies(response)
            flash("Conta excluída com sucesso.", category="success")
            return response
        else:
            flash(
                "Senha incorreta. Conta não foi excluída.",
                category="danger"
            )

    return redirect(url_for("users.profile_page"))

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']

        # Monta o link para redefinir a senha
        link_redefinir = 'http://127.0.0.1:59436/changing_password'  # ou o seu domínio real

        # Envia o email de recuperação
        assunto = 'Recuperação de Senha - MoneyWise'
        corpo = f'''
        <h2>Recuperação de Senha - MoneyWise</h2>
        <p>Olá!</p>
        <p>Recebemos uma solicitação para redefinir a sua senha. Se você pediu essa alteração, clique no botão abaixo:</p>
        <br>
        <a href="{link_redefinir}" style="padding: 10px 20px; background-color: #7E9DCA; color: white; text-decoration: none; border-radius: 5px;">Redefinir Senha</a>
        <br><br>
        <p>Se você não solicitou a redefinição, pode ignorar este email. Sua senha continuará a mesma.</p>
        <p>Atenciosamente,<br><strong>Equipe MoneyWise</strong></p>
        '''
        enviar_email(email, assunto, corpo)

        flash('Um email de recuperação foi enviado!', 'success')
        return redirect(url_for('users.signin_page')) 

    return render_template('reset_password_page.html')


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirmar_senha']

        if nova_senha != confirmar_senha:
            flash('As senhas não coincidem.', 'danger')
            return redirect(request.url)

        # Aqui no futuro: validar o token e alterar a senha do usuário no banco de dados

        flash('Senha alterada com sucesso! Faça login.', 'success')
        return redirect(url_for('users.signin_page'))

    return render_template('changing_password_page.html')

@users.route('/changing_password', methods=['GET', 'POST'])
def changing_password():
    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirmar_senha']

        if nova_senha != confirmar_senha:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('users.changing_password'))

        # Aqui você salvaria a nova senha no banco de dados (depois configuramos isso)
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('users.signin_page'))

    return render_template('changing_password_page.html')