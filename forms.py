from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileRequired, FileField

class UPCForm(FlaskForm):
    upc = StringField('UPC number', validators=[DataRequired(), Length(max=12)])
    image = FileField('Image file')
    submit = SubmitField('Look up')
    barcode_submit = SubmitField('Scan barcode and look up')

class UPCFileForm(FlaskForm):
    image = FileField('Image file', validators=[FileRequired()])
    submit = SubmitField('Look up')

class UPCStringForm(FlaskForm):
    upc = StringField('UPC number', validators=[DataRequired(), Length(max=12)])
    submit = SubmitField('Look up')