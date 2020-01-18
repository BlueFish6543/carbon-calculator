from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class UPCForm(FlaskForm):
    upc = IntegerField('UPC number', validators=[DataRequired(), Length(min=12, max=12)])
    submit = SubmitField('Look up')