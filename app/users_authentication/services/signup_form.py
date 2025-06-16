from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError
)
from app.users_authentication.models import User


class UserSignupForm(FlaskForm):
    username = StringField(
        "Usuário:",
        validators=[Length(min=3, max=30), DataRequired()],
    )
    email_address = StringField(
        "Email:",
        validators=[Email(), DataRequired()],
    )
    password = PasswordField(
        "Senha:",
        validators=[DataRequired()],
    )
    confirm_password = PasswordField(
        "Confirmar Senha:",
        validators=[
            DataRequired(),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    birthday = DateField(
        "Aniversário:",
        format="%Y-%m-%d",
        validators=[DataRequired()],
    )

    submit = SubmitField("Criar Conta")

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError("Usuário já cadastrado.")

    def validate_email_address(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email já cadastrado.")

    def validate_password(self, field):
        pwd = field.data

        if len(pwd) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if not any(c.isalpha() for c in pwd):
            raise ValidationError("A senha deve conter pelo menos uma letra.")
        if not any(c.isdigit() for c in pwd):
            raise ValidationError("A senha deve conter pelo menos um número.")

        special_characters = "!@#$%^&*()-_+=<>?/|{}[]:;'"
        if not any(c in special_characters for c in pwd):
            raise ValidationError(
                "A senha deve conter pelo menos um caractere especial."
            )
