from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from . import db
from .forms import ArgumentForm
from .model import Argument, Product, Company
from flask_login import login_required, current_user
from base64 import b64encode

bp = Blueprint('argument', __name__, url_prefix='/argument')

@bp.route('/')
def list_argument():
    args=Argument.query.order_by(Argument.date_created.desc()).limit(5)
    return render_template("argument/list.html", args=args)

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_argument():
    form = ArgumentForm()
    form.pro_product.choices = prod_choices
    form.con_product.choices = prod_choices
    if form.validate_on_submit():
        pass
    prod_choices = [(p.id, f"{p.name} ({p.Company.name})") for p in Product.query.all()]
    
    pro_get = request.args.get('pro', default=None, type=int)
    con_get = request.args.get('con', default=None, type=int)
    if pro_get is not None:
        form.pro_product.data = str(pro_get)
    if con_get is not None:
        form.con_product.data = str(con_get)

    return render_template("argument/add.html", form=form)