from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class databaseConfigurationForm(FlaskForm):
    db_file = FileField('Database File')
    add_data = SubmitField('Add Data')