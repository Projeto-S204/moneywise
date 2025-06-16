from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        label="Senha:",
        validators=[
            DataRequired(),
            Length(min=8, message="A senha deve ter pelo menos 8 caracteres.")
        ],
    )
    confirm_password = PasswordField(
        label="Confirmar Senha:",
        validators=[
            DataRequired(),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField("Redefinir senha")

    def validate_password(self, field):
        pwd = field.data

        if not any(c.isalpha() for c in pwd):
            raise ValidationError("A senha deve conter pelo menos uma letra.")
        if not any(c.isdigit() for c in pwd):
            raise ValidationError("A senha deve conter pelo menos um número.")
        special_characters = "!@#$%^&*()-_+=<>?/|{}[]:;'"
        if not any(c in special_characters for c in pwd):
            raise ValidationError(
                "A senha deve conter pelo menos um caractere especial.")
