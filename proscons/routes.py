from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from .model import Argument

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route("/")
def index():
    args=Argument.query.order_by(Argument.date_created.desc()).limit(5).all()
    return render_template("index.html", args=args)