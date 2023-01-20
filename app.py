from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import configparser as cp

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

login_manager = LoginManager()

# "strong" means that if the user's session is manipulated or modified, the user will be
# logged out. This provides an extra layer of security.
login_manager.session_protection = "strong"

# Sets the view function for handling failed attemps (is the "login" function in the routes.py file)
# This means that if an user fails to log in they will be redirected to the login function in routes.py
# It also means that if an user tries to access a protected view without being logged in they will be redirected.
login_manager.login_view = "login"

# There are different categories, info, error, etc. It styles the flash messages according to the category
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app() -> Flask:
    config = cp.ConfigParser()
    config.read('config.ini')

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['DB_URI']
    app.config['SECRET_KEY'] = config['FLASK']['SECRET_KEY']

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
