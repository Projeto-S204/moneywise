from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
)
from app.users_authentication.models import User


class UserSignupForm(FlaskForm):
    username = StringField(
        label="UserName:",
        validators=[Length(min=3, max=30), DataRequired()],
    )
    email_address = StringField(
        label="Email:", validators=[Email(), DataRequired()],
    )
    password = PasswordField(
        label="Password:", validators=[DataRequired()],
    )
    confirm_password = PasswordField(
        label="Confirm Password:",
        validators=[
            EqualTo("password", message="As senhas não coincidem."),
            DataRequired(),
        ],
    )
    birthday = DateField(
        "Birthday:", format="%Y-%m-%d", validators=[DataRequired()]
    )

    submit = SubmitField(label="Criar Conta")

    # avatar = FileField("Avatar URL (Optional):")

    def validate_username(self, username_to_check):
        user = User.query.filter_by(
            name=username_to_check.data
        ).first()
        if user:
            raise ValidationError("Usuário já cadastrado.")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email=email_address_to_check.data
        ).first()
        if email_address:
            raise ValidationError("Email já cadastrado.")

    def validate_password(self, password_to_check):
        if len(password_to_check.data) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if not any(c.isalpha() for c in password_to_check.data):
            raise ValidationError("A senha deve conter pelo menos uma letra.")
        if not any(c.isalnum() for c in password_to_check.data):
            raise ValidationError("A senha deve conter pelo menos um número.")

        special_characters = "!@#$%^&*()-_+=<>?/|{}[]:;'"

        if not any(c in special_characters for c in password_to_check.data):
            raise ValidationError(
                "A senha deve conter pelo menos um caractere especial."
            )
