from proscons import db
from flask_login import UserMixin
from . import login

# Eigententwicklung / Übernommen
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean)
    companies_created = db.relationship('Company', backref='user_created', lazy=True)
    products_created = db.relationship('Product', backref='user_created', lazy=True)
    arguments_created = db.relationship('Argument', backref='user_created', lazy=True)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
# Eigententwicklung
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    country = db.Column(db.String, nullable=False)
    products = db.relationship('Product', backref="company", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Eigententwicklung
class Argument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    pro_prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    con_prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

# Eigententwicklung
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    image = db.Column(db.LargeBinary)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    # https://stackoverflow.com/a/5652169
    pro_args = db.relationship(
        'Argument',
        primaryjoin=Argument.pro_prod_id==id,
        backref="pro_prod"
    )
    con_args = db.relationship(
        'Argument',
        primaryjoin=Argument.con_prod_id==id,
        backref="con_prod"
    )
