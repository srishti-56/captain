import sys
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy #This is an ORM. 
from flask_login import LoginManager


# instantiate the db object
db = SQLAlchemy()

# instantiate the login object
login_manager = LoginManager()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # Set up Login
    app.secret_key = 'somethingsecret'
    login_manager.login_view = "login"
    login_manager.session_protection = "strong"

    login_manager.init_app(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:postgres@users-db:5432/users"
    # set up extensions
    db.init_app(app)


    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # shell context for flask cli (allows working with the application context and the database without having to import them directly into the shell)
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
