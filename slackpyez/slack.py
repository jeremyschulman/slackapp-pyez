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

import os
import json
from pathlib import Path
import toml

from slackpyez.callback_handler import CallbackHandler
from slackpyez.request import SlackRequest
from slackpyez.log import create_logger
from slackpyez.sessions import SlackAppSessionInterface


class SlackAppConfig(dict):
    def __init__(self):
        super(SlackAppConfig, self).__init__()
        self.channels = None
        self.data = None

    def from_envar(self, envar):
        conf_file = os.environ.get(envar)
        if not conf_file:
            raise RuntimeError(f'The environment variable {envar} is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file')

        conf_file_p = Path(conf_file)
        if not conf_file_p.exists():
            raise RuntimeError(f'The environment variable {envar} is set to '
                               f'{conf_file}, but this file does not exist')

        self.data = toml.load(conf_file_p)

        self.channels = {_chan['id']: _chan
                         for _chan in self.data['channel']}

        self['ALL_SLACK_VERIFY_TOKENS'] = [
            _chan['verify_token']
            for _chan in self.data['channel']
        ]

        self['SLACK_CHANNEL_NAME_TO_ID'] = {
            _chan['name']: _chan['id']
            for _chan in self.data['channel']
        }


class SlackApp(object):

    def __init__(self):
        self.log = create_logger()

        self.on_block_actions = CallbackHandler('block_id')
        self.on_dialog_submit = CallbackHandler('callback_id')
        self.on_imsg = CallbackHandler('callback_id')

        self.on_payload_type = CallbackHandler('type')

        self.config = SlackAppConfig()

        # setup the default handler functions

        self.on_payload_type['block_actions'] = self._handle_block_actions
        self.on_payload_type['dialog_submission'] = self._handle_dialog_submit
        self.on_payload_type['interactive_message'] = self._handle_imsg

    @staticmethod
    def register_app(flaskapp, sessiondb_path):
        flaskapp.session_interface = SlackAppSessionInterface(sessiondb_path)

    def register_block_action(self, key, func):
        self.on_block_actions[key] = func

    def register_dialog_submit(self, callback_id, func):
        self.on_dialog_submit[callback_id] = func

    def request(self, rqst_form):
        return SlackRequest(app=self, rqst_data=rqst_form)

    # -------------------------------------------------------------------------
    # request handlers
    # -------------------------------------------------------------------------

    def _handle_block_actions(self, rqst):
        action = rqst.payload['actions'][0]
        callback = self.on_block_actions.callback_for(action)
        return callback(rqst, action)

    def _handle_dialog_submit(self, rqst):
        callback = self.on_dialog_submit.callback_for(rqst.payload)
        return callback(rqst, rqst.payload['submission'])

    def _handle_imsg(self, rqst):
        callback = self.on_imsg.callback_for(rqst.payload)
        return callback(rqst, rqst.payload['actions'][0])

    def handle_request(self, form_data):
        rqst = self.request(form_data)

        self.log.info("PAYLOAD>> {}\n".format(json.dumps(rqst.payload, indent=3)))

        callback = self.on_payload_type.callback_for(rqst.payload)
        return callback(rqst)
