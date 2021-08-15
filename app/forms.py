from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, RadioField, IntegerField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, DataRequired
from wtforms.widgets import HiddenInput
from app import db
