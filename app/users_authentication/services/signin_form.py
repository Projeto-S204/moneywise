from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class UserSigninForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Senha:", validators=[DataRequired()])
    submit = SubmitField("Login")
