from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, FileField
from wtforms.validators import InputRequired


class AccountForm(FlaskForm):
    address = StringField('HNT Wallet Address', validators=[InputRequired()])
    submit_account = SubmitField(label='Export CSV')


class HotspotForm(FlaskForm):
    address = StringField('Hotspot Address', validators=[InputRequired()])
    submit_hotspot = SubmitField(label='Export CSV')