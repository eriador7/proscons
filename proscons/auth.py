from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, RegisterForm
from .model import User
from password_strength import PasswordStats
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Übernommen
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user:User = User.query.filter_by(username=form.username.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("Incorrect username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        if not next or url_parse(next).netloc != '':
            return redirect(url_for("index.index"))
        return redirect(next)
    return render_template('auth/login.html', form=form)

@bp.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Successfully logged out")
    else:
        flash("You'd need to login first to logout...")
    return redirect(url_for("index.index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Already registered...")
        return redirect(url_for("index.index"))
    form = RegisterForm()    
    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.email = form.email.data
        new_user.password = generate_password_hash(form.password.data)
        new_user.is_admin = False
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Successfully registered")
        return redirect(url_for("index.index"))
    return render_template("auth/register.html", form=form)
