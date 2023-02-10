import os, click
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask, current_app
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
from .model import *

# Eigenentwicklung
def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_prefixed_env()

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    app.cli.add_command(init_db_command)

    # Blueprints: https://flask.palletsprojects.com/en/2.2.x/tutorial/views/
    """
    A Blueprint is a way to organize a group of related views and other code. Rather than registering 
    iews and other code directly with an application, they are registered with a blueprint. Then the
    blueprint is registered with the application when it is available in the factory function.
    """
    from . import auth
    app.register_blueprint(auth.bp)

    from . import routes
    app.register_blueprint(routes.bp)

    from . import product
    app.register_blueprint(product.bp)

    return app

#Eigententwicklung
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    admin_user = User()
    admin_user.username = "admin"
    admin_user.email = "admin@localhost"
    pwd = current_app.config['ADMIN_PWD'] or "changeme"
    admin_user.password = generate_password_hash(pwd)
    admin_user.is_admin = True
    db.session.add(admin_user)
    db.session.commit()
    click.echo('Initialized the database.')

