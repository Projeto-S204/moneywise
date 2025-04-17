from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify,
    flash,
    make_response,
)
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
    # verify_jwt_in_request,
    get_jwt_identity,
    # create_refresh_token,
)
from app.users_authentication.services.signin_form import UserSigninForm
from app.users_authentication.services.signup_form import UserSignupForm
from app.users_authentication.services.form_validations import (
    validate_form_on_signup,
    validade_form_on_signin,
)
from flask_login import logout_user


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
    if form.is_submitted():
        user = validade_form_on_signin(form)
        if user:
            access_token = create_access_token(identity=str(user.id))
            print(f"[ROTA] Token com Flask-JWT-Extended: {access_token}")
            response = make_response(
                redirect(url_for("transactions.transactions_page"))
            )
            set_access_cookies(response, access_token)
            flash("Login bem-sucedido!", "success")
            return response

    return render_template("signin_page.html", form=form)


@users.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = UserSignupForm()
    if form.is_submitted():
        user = validate_form_on_signup(form)
        if user:
            access_token = create_access_token(identity=str(user.id))
            print(f"[ROTA] Token com Flask-JWT-Extended: {access_token}")
            response = make_response(redirect(url_for("users.signin_page")))
            set_access_cookies(response, access_token)
            return response

    return render_template("signup_page.html", form=form)


@users.route("/logout")
#  @jwt_required()
def logout():
    logout_user()
    response = make_response(redirect(url_for("users.signin_page")))
    unset_jwt_cookies(response)
    flash("Logout realizado com sucesso!", "success")
    return response


@users.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    print(f"[PROTECTED] Acesso com user_id: {current_user_id}")
    return jsonify(msg="Acesso autorizado!", user_id=current_user_id)
