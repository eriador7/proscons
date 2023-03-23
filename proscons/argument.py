#Eigententwicklung

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from . import db
from .forms import ArgumentForm
from .model import Argument, Product, User
from flask_login import login_required, current_user
from base64 import b64encode
from datetime import datetime

bp = Blueprint('argument', __name__, url_prefix='/argument')

@bp.route('/')
def list_arguments():
    products = Product.query.order_by(Product.name).all()
    pro_id = request.args.get("pro", default=None, type=int)
    con_id = request.args.get("con", default=None, type=int)
    return render_template(
        "argument/list.html",
        products=products,
        selected_pro = pro_id,
        selected_con = con_id
    )

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_argument():
    prod_choices = [(p.id, f"{p.name} ({p.company.name})") for p in Product.query.all()]
    prod_choices.insert(0, (None, "-- Please Select --"))
    form = ArgumentForm()
    form.pro_product.choices = prod_choices
    form.con_product.choices = prod_choices
    if form.validate_on_submit():
        arg = Argument()
        arg.pro_prod_id = form.pro_product.data
        arg.con_prod_id = form.con_product.data
        arg.comment = form.comment.data
        arg.date_created = datetime.now()
        arg.user_id = current_user.id
        db.session.add(arg)
        db.session.commit()
        return redirect(url_for("argument.list_arguments", pro=arg.pro_prod_id, con=arg.con_prod_id))
    
    pro_get = request.args.get('pro', default=None, type=int)
    con_get = request.args.get('con', default=None, type=int)
    if pro_get is not None:
        form.pro_product.data = str(pro_get)
    if con_get is not None:
        form.con_product.data = str(con_get)

    return render_template("argument/add.html", form=form)

@bp.route("/edit/<argumentid>", methods=["GET", "POST"])
@login_required
def edit_argument(argumentid):
    arg = Argument.query.get(argumentid)
    if not arg:
        return abort(404)
    curr_user = User.query.get(current_user.get_id())
    if not (curr_user.is_admin or curr_user.id == arg.user_created.id):
        return abort(401)
    prod_choices = [(p.id, f"{p.name} ({p.company.name})") for p in Product.query.all()]
    prod_choices.insert(0, (None, "-- Please Select --"))
    form = ArgumentForm(obj=arg)
    form.pro_product.choices = prod_choices
    form.con_product.choices = prod_choices
    if form.validate_on_submit():
        arg.comment = form.comment.data
        arg.con_prod_id = form.con_product.data
        arg.pro_prod_id = form.pro_product.data
        db.session.commit()
        flash("Updated argument successfully")
        return redirect(url_for("argument.list_arguments", pro=arg.pro_prod_id, con=arg.con_prod_id))
    form.pro_product.data = str(arg.pro_prod_id)
    form.con_product.data = str(arg.con_prod_id)
    return render_template("argument/edit.html", form=form)
