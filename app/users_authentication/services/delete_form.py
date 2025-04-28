from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class UserDeleteForm(FlaskForm):
    password = PasswordField("Confirme sua senha", validators=[DataRequired()])
    submit = SubmitField("Excluir Conta")
