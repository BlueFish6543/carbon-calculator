from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length

class UPCForm(FlaskForm):
    upc = StringField('UPC number', validators=[DataRequired(), Length(max=12)])
    image = FileField('Image File')
    submit = SubmitField('Look up')

class UPCFileForm(FlaskForm):
    image = FileField('Image File', validators=[DataRequired()])
    submit = SubmitField('Look up')

class UPCStringForm(FlaskForm):
    upc = StringField('UPC number', validators=[DataRequired(), Length(max=12)])
    submit = SubmitField('Look up')