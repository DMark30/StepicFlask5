from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class RegisterForm(FlaskForm):
    clientEmail = StringField("Электропочта", [DataRequired(), Email(), Length(max=100)], render_kw={'autofocus': True})
    clientPassword = PasswordField("Пароль", [DataRequired(), Length(min=8, message='Пароль должен состоять хотя бы '
                                                                                   'из %(min)d символов')])

class OrderForm(FlaskForm):
    clientName = StringField("Ваше имя", [DataRequired()])
    clientEmail = StringField("Электропочта", [DataRequired(), Email(), Length(max=100)], render_kw={'autofocus': True})
    clientAddress = StringField("Адрес", [DataRequired()])
    clientPhone = StringField("Телефон", [DataRequired()])
