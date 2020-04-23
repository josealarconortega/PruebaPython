
from flask import Flask

from application.api.database import db_init
from config import app_config

from application.api.routes import mod as apimod


def create_app(config_name: str):
    '''Initialize the core application.'''
    app = Flask(__name__, instance_relative_config=False,
                static_folder='site/dist/static')
    app.config.from_object(app_config[config_name])

    with app.app_context():

        db_init(app)

        app.register_blueprint(apimod, url_prefix='/searchEarthquake')

        # # Include our Routes
        # from . import routes

        # # Include our Routes
        # from . import models

        return app
