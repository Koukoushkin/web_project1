from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    passw = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
