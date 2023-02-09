from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from . import db
from .model import Company

# Übernommen
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Eigententwicklung
class ProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    company = SelectField("Company")
    
# Eigenentwicklung    
class CompanyForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    country = StringField("Home country")
    image = FileField("Company logo")

# Eigententwicklung
class Argument(FlaskForm):
    pass
