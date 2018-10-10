import sys
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy #This is an ORM. 

# instantiate the db object
db = SQLAlchemy()

def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

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
