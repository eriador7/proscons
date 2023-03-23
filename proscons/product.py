# Eigenentwicklung

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from . import db
from .forms import ProductForm
from .model import Company, Product, User
from flask_login import login_required, current_user
from base64 import b64encode

bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route('/')
def list_products():
    return render_template("product/list.html", products=Product.query.order_by(Product.name).all())

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    form.company.choices = [(c.id, c.name) for c in Company.query.order_by(Company.name).all()]
    if form.validate_on_submit():
        p = Product()
        p.description = form.description.data
        p.company_id = form.company.data
        p.name = form.name.data
        p.user_id = current_user.id
        p.image = form.image.data.stream.read()
        db.session.add(p)
        db.session.commit()
        flash(f"Successfully created {p.name}")
        return redirect(url_for("product.list_products"))
    form.company.choices.insert(0, (None, "-- Please select --"))
    return render_template("product/add.html", form=form)

@bp.route("/edit/<productid>", methods=["GET", "POST"])
@login_required
def edit_product(productid):
    prod = db.session.query(Product).get(productid)
    if not prod:
        return abort(404)
    curr_user = User.query.get(current_user.get_id())
    if not (curr_user.is_admin or curr_user.id == prod.user_id):
        return abort(401)
    form = ProductForm(obj=prod)
    form.company.choices = [(c.id, c.name) for c in Company.query.order_by(Company.name).all()]
    if form.validate_on_submit():
        prod.description = form.description.data
        prod.company_id = form.company.data
        prod.name = form.name.data
        if form.image.data:
            prod.image = form.image.data.stream.read()
        db.session.commit()
        flash("Saved changes")
        return redirect(url_for("product.list_products"))
    form.company.data = str(prod.company_id)
    imgdata = None
    if prod.image:
        imgdata = b64encode(prod.image).decode()
    return render_template("product/edit.html", form=form, id=prod.id, imgdata=imgdata)