from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class UPCForm(FlaskForm):
    upc = StringField('UPC number', validators=[DataRequired(), Length(min=12, max=12)])
    submit = SubmitField('Look up')