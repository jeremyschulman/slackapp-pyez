#  Copyright 2019 Jeremy Schulman, nwkautomaniac@gmail.com
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#  http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from flask import Flask
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
