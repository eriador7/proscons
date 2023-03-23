from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileAllowed
from .model import User
from password_strength import PasswordStats
from flask import Markup

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
    # Quelle (Markup): https://stackoverflow.com/questions/58534459/how-to-render-make-clickable-a-url-in-a-stringfield-using-wtforms
    password = PasswordField('Password', description=Markup("<a href=\"https://xkcd.com/936/\" target=\"_blank\">How to choose a good password</a>"), validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(form, field):
        check_user_exists = User.query.filter_by(username=field.data).scalar()
        if check_user_exists:
            raise ValidationError("Username already registered")

    def validate_email(form, field):
        check_email_exists = User.query.filter_by(email=field.data).scalar()
        if check_email_exists:
            raise ValidationError("E-Mail address already registered")

    # Require a strong password, however instead of the usual way
    # we chose a reasonable check to verify whether the provided
    # password is strong --> Entropy. Ref: https://xkcd.com/936/
    def validate_password(form, field):
        ent = PasswordStats(field.data).entropy_bits
        if ent < 30:
            raise ValidationError("Your password is too weak, try making it longer or add more different \
                symbols/numbers/characters.")

# Eigententwicklung
class ProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    company = SelectField("Company")
    image = FileField("Product logo", validators=[FileAllowed(['png'], "Only png images allowed")])
    submit = SubmitField()

    def validate_company(form, field):
        if field.data == "None":
            raise ValidationError("Please select a value")
    
# Eigenentwicklung    
class CompanyForm(FlaskForm):
    name = StringField("Company name", validators=[DataRequired()])
    country = StringField("Home country")
    description = StringField()
    submit = SubmitField()


# Eigententwicklung
class ArgumentForm(FlaskForm):
    pro_product = SelectField("Pro Product")
    con_product = SelectField("Con Product")
    comment = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField()

    def validate_con_product(form, field):
        if field.data == "None":
            raise ValidationError("Please select a value")
        if field.data == form.pro_product.data:
            raise ValidationError("Pro and con product cannot be the same")

    def validate_pro_product(form, field):
        if field.data == "None":
            raise ValidationError("Please select a value")
