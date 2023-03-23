# Eigenentwicklung

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from . import db
from .forms import CompanyForm
from .model import Company, User
from flask_login import login_required, current_user

bp = Blueprint('company', __name__, url_prefix='/company')

@bp.route('/')
def list_companies():
    return render_template("company/list.html", companies=Company.query.order_by(Company.name).all())

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_company():
    form = CompanyForm()
    form.submit.label.text = "Add Company"
    if form.validate_on_submit():
        c = Company()
        c.country = form.country.data
        c.description = form.description.data
        c.name = form.name.data
        c.user_id = current_user.id
        db.session.add(c)
        db.session.commit()
        flash(f"Successfully created {c.name}")
        return redirect(url_for("company.list_companies"))
    return render_template("company/add.html", form=form)

@bp.route("/edit/<companyid>", methods=["GET", "POST"])
@login_required
def edit_company(companyid):
    comp = db.session.query(Company).get(companyid)
    if not comp:
        return abort(404)
    curr_user = User.query.get(current_user.get_id())
    if not (curr_user.is_admin or curr_user.id == comp.user_id):
        return abort(401)
    form = CompanyForm(obj=comp)
    form.submit.label.text = "Update Company"
    if form.validate_on_submit():
        comp.description = form.description.data
        comp.country = form.country.data
        comp.name = form.name.data
        db.session.commit()
        flash("Saved changes")
        return redirect(url_for('company.list_companies'))
    return render_template("company/edit.html", form=form, id=comp.id)