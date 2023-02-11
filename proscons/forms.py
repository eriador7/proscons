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
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

# Eigententwicklung
class ProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    company = SelectField("Company")
    image = FileField("Product logo")
    submit = SubmitField()
    
# Eigenentwicklung    
class CompanyForm(FlaskForm):
    name = StringField("Company name", validators=[DataRequired()])
    country = StringField("Home country")
    description = StringField()
    submit = SubmitField()


# Eigententwicklung
class Argument(FlaskForm):
    pass
