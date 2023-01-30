from flask import Flask
import configparser as cp

from .extensions import db, login_manager, migrate, bcrypt
from .routes import main

# "strong" means that if the user's session is manipulated or modified, the user will be
# logged out. This provides an extra layer of security.
login_manager.session_protection = "strong"

# Sets the view function for handling failed attemps (is the "login" function in the routes.py file)
# This means that if an user fails to log in they will be redirected to the login function in routes.py
# It also means that if an user tries to access a protected view without being logged in they will be redirected.
login_manager.login_view = "login"

# There are different categories, info, error, etc. It styles the flash messages according to the category
login_manager.login_message_category = "info"

# TODO: add testing variables in config.ini
def create_app(testing=False):
    config = cp.ConfigParser()
    config.read('/app/project/config.ini')

    app = Flask(__name__)

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_TESTING']['DB_URI']
        app.config['SECRET_KEY'] = config['FLASK_TESTING']['SECRET_KEY']
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_PRODUCTION']['DB_URI']
        app.config['SECRET_KEY'] = config['FLASK_PRODUCTION']['SECRET_KEY']


    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    app.register_blueprint(main)

    return app