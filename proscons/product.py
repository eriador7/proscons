from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from . import db
from .forms import ProductForm
from .model import Company, Product

bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route("/add")
def add_product():
    form = ProductForm()
    form.company.choices = [(c.id, c.name) for c in db.session.execute(db.select(Company).order_by(Company.name)).scalars()]
    return render_template("product/add_update.html", form=form)

@bp.route("/edit/<productid>")
def edit_product(productid):
    prod = db.session.query(Product).get(productid)
    form = ProductForm(obj=prod)
    form.company.choices = [(c.id, c.name) for c in db.session.execute(db.select(Company).order_by(Company.name)).scalars()]
    form.company.data = prod.company_id
    return render_template("product/edit.html", form=form)