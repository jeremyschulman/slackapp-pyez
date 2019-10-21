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

import json
from importlib import import_module
import api

from first import first
from flask import Flask, jsonify
from blueprint import blueprint

from slackpyez import SlackAppError, SlackAppApiError
from slackpyez.slackapi import SlackApiResponse
from slackpyez.ui import BLOCKS

from app_data import (
    slackapp,
    create_event_adapter,
    register_flaskapp
)


def create_app():

    app = register_flaskapp(Flask(__name__))
    app.config.from_envvar('FLASKAPP_SETTINGS')

    # -------------------------------------------------------------------------
    # Setup our Slackapp client
    # -------------------------------------------------------------------------

    slackapp.config.from_envar('SLACKAPP_SETTINGS')
    slackapp.register_app(flaskapp=app,
                          sessiondb_path=slackapp.config['sessions']['path'])

    channel_id = first(slackapp.config.channels)
    secret = slackapp.config.channels[channel_id]['signing_secret']
    create_event_adapter(flaskapp=app, secret=secret)

    # -------------------------------------------------------------------------
    # now register all the API routes and Slack event handlers
    # -------------------------------------------------------------------------

    app.register_blueprint(blueprint)
    for route in app.url_map.iter_rules():
        print(route)

    app.register_error_handler(SlackAppError, on_401_unauthorized)
    return app


def on_401_unauthorized(exc):
    if isinstance(exc,SlackAppApiError):
        api_resp = exc.args[0]
        emsg = json.dumps(api_resp.resp, indent=3)
        api_error = api_resp.resp.get('error') or 'error=n/a'
        slackapp.log.error(f"SlackAppApiError {api_error} payload>>\n{emsg}\n")
        return ""

    if isinstance(exc, SlackApiResponse):
        errmsg = "Call to SlackAPI failed: {}".format(exc.resp)
        slackapp.log.error(errmsg)
        err = dict(blocks=[BLOCKS.section(errmsg)])
        return jsonify(err)

    try:
        msg, code, rqst = exc.args

    except Exception as exc:
        errmsg = "App error called with exception: {}".format(str(exc))
        slackapp.log.error(errmsg)
        err = dict(blocks=[BLOCKS.section(errmsg)])
        return jsonify(err)

    msg = dict(
        blocks=[BLOCKS.section(
            f"I'm sorry {rqst.user_name}, I'm not authorized do to that."
        )]
    )
    return jsonify(msg)
