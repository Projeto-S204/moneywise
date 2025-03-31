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
        validators=[Length(min=2, max=30), DataRequired()],
    )
    email_address = StringField(
        label="Email:", validators=[Email(), DataRequired()],
    )
    password = PasswordField(
        label="Password:", validators=[Length(min=6), DataRequired()],
    )
    confirm_password = PasswordField(
        label="Confirm Password:",
        validators=[EqualTo("password"), DataRequired()],
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
