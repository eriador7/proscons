from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
from . import db
from .forms import ArgumentForm
from .model import Argument, Product, Company
from flask_login import login_required, current_user
from base64 import b64encode
from datetime import datetime

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("compare")
def compare_products():
    errs = []
    pro_id = request.args.get("pro", default=None, type=int)
    con_id = request.args.get("con", default=None, type=int)
    if pro_id is None:
        errs.append("GET parameter 'pro' not set")
    else:
        pro = Product.query.get(pro_id)
        if not pro:
            errs.append(f"Product with id {pro_id} not found")
    if con_id is None:
        errs.append("GET parameter 'con' not set")
    else:
        con = Product.query.get(con_id)
        if not pro:
            errs.append(f"Product with id {con_id} not found")
    if pro_id is not None and pro_id == con_id:
        errs.append("'pro' and 'con' parameters cannot be the same value")
    
    if errs:
        return {"errors":errs}, 400
    
    # TODO: Ordering
    args = [arg.to_dict(is_pro=True) for arg in pro.pro_args if arg.con_prod.id == con.id]
    args.extend([arg.to_dict(is_con=True) for arg in pro.con_args if arg.pro_prod.id == con.id])
    return jsonify(args)

@bp.route("products")
def get_products():
    products = Product.query.order_by(Product.name).all()
    return jsonify([p.to_dict() for p in products])

@bp.route("products/<prodid>")
def get_product(prodid):
    prod = Product.query.get(prodid)
    if not prod:
        return {"error":f"Product with id {prodid} not found"}, 404
    return jsonify(prod.to_dict(include_image=True))