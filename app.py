from flask import Flask
from flaskApp.settings import config
from flaskApp.extensions import db, migrate
from flaskApp.models import StatisticData
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask('nCoA')
    app.config.from_object(config[config_name])
    register_extensions(app)
    # register_commands(app)
    # register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    # login_manager.init_app(app)

# def register_blueprints(app):
#     app.register_blueprint(station_bp)
#     app.register_blueprint(auth_bp)


# from todolist import commands, views
# from chargeStationStatus import commands, models, views
