from flask import Flask
from importlib import import_module
import api
from blueprint import blueprint


def register_blueprint_routes(app):
    app.register_blueprint(blueprint)
    for route in app.url_map.iter_rules():
        print(route)


def create_app():
    from slackapp import slackapp

    app = Flask(__name__)
    app.config.from_envvar('FLASKAPP_SETTINGS')
    register_blueprint_routes(app)
    slackapp.config.from_envar('SLACKAPP_SETTINGS')

    return app
