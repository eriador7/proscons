import os, click, base64
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask, current_app, app
from werkzeug.security import generate_password_hash
from flask_bootstrap import Bootstrap

# Hauptsächlich übernommen
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
from .model import *


# Teilweise eigenentwicklung
def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_prefixed_env()

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    Bootstrap(app)

    app.cli.add_command(init_db_command)
    app.cli.add_command(reset_all_passwords)

    # Blueprints: https://flask.palletsprojects.com/en/2.2.x/tutorial/views/
    """
    A Blueprint is a way to organize a group of related views and other code. Rather than registering 
    views and other code directly with an application, they are registered with a blueprint. Then the
    blueprint is registered with the application when it is available in the factory function.
    """
    from . import auth
    app.register_blueprint(auth.bp)

    from . import routes
    app.register_blueprint(routes.bp)

    from . import company
    app.register_blueprint(company.bp)

    from . import product
    app.register_blueprint(product.bp)

    from . import argument
    app.register_blueprint(argument.bp)

    from . import api
    app.register_blueprint(api.bp)

    app.add_template_filter(b64encode)

    return app

def b64encode(s):
    return base64.b64encode(s).decode()

#Eigententwicklung
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    """
    admin_user = User()
    admin_user.username = "admin"
    admin_user.email = "admin@localhost"
    pwd = current_app.config['ADMIN_PWD'] or "changeme"
    admin_user.password = generate_password_hash(pwd)
    admin_user.is_admin = True
    db.session.add(admin_user)
    db.session.commit()
    click.echo('Initialized the database.')
    """
    cmd = open("data.sql", "r").read()
    db.session.execute(text(cmd))
    db.session.commit()
    # update passwords
    
#Eigenentwicklung
@click.command('pwd-reset')
def reset_all_passwords():
    pwd = current_app.config['ADMIN_PWD'] or "changeme"
    for user in User.query.all():
        user.password = generate_password_hash(pwd)
    db.session.commit()

