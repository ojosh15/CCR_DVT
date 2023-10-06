from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class databaseConfigurationForm(FlaskForm):
    db_file = FileField('Database File')
    add_data = SubmitField('Add Data')
    
class analysisConfigurationForm(FlaskForm):
    serial_number = SelectField('CCR Serial Number:', coerce=int)
    unit = RadioField('Select a Unit:', choices=[('main','Main'),('interface','Interface'),('expansion','Expansion')],default='main')
    
class settingsForm(FlaskForm):
    submit = SubmitField('Save Settings')
    
class componentForm(FlaskForm):
    model = StringField('Model:',validators=[DataRequired(), Length(max=50)])
    comp_type = StringField('Type:',validators=[DataRequired(), Length(max=50)])
    manufacturer = StringField('Manufacturer:',validators=[DataRequired(), Length(max=50)])
    active = BooleanField('Active:')
    source = SelectField('Data Source:',coerce=str,choices=['Measured','Simulated','Manufacturer Provided'])
    submit = SubmitField('Add Component')