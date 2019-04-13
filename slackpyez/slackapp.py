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
from collections import UserDict

import toml
from first import first
import pyee
from slackclient import SlackClient

from slackpyez.request import SlackRequest
from slackpyez.log import create_logger
from slackpyez.sessions import SlackAppSessionInterface
from slackpyez import ui, exc


__all__ = ['SlackApp', 'SlackAppConfig']


class SlackAppConfig(UserDict):

    def __init__(self):
        super(SlackAppConfig, self).__init__()
        self.channels = None

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

        # store the config file data into the object as dict

        self.update(toml.load(conf_file_p))

        # create a specific `channels` attribute that is a dict of channel ID to
        # channel config.

        self.channels = {_chan['id']: _chan
                         for _chan in self['channel']}

        self['ALL_SLACK_VERIFY_TOKENS'] = [
            _chan['verify_token']
            for _chan in self['channel']
        ]

        self['SLACK_CHANNEL_NAME_TO_ID'] = {
            _chan['name']: _chan['id']
            for _chan in self['channel']
        }


class SlackApp(object):

    def __init__(self):
        self.log = create_logger()

        self.ux_block = pyee.EventEmitter()
        self.ux_dialog = pyee.EventEmitter()
        self.ux_imsg = pyee.EventEmitter()

        self._in_msg = pyee.EventEmitter()

        self._in_msg.on('block_actions', self._handle_block_actions)
        self._in_msg.on('dialog_submission', self._handle_dialog_submit)
        self._in_msg.on('interactive_message', self._handle_imsg)

        self.config = SlackAppConfig()

        # setup the default handler functions

    @staticmethod
    def register_app(flaskapp, sessiondb_path):
        flaskapp.session_interface = SlackAppSessionInterface(sessiondb_path)

    def request(self, rqst_form):
        return SlackRequest(app=self, rqst_data=rqst_form)

    def create_client(self, channel=None, chan_id=None, as_bot=False):
        chan_id = (chan_id or (
            self.config['SLACK_CHANNEL_NAME_TO_ID'][channel] if channel
            else first(self.config.channels)))

        chan_cfg = self.config.channels[chan_id]
        token = chan_cfg['oauth_token' if not as_bot else 'bot_oauth_token']
        return SlackClient(token=token)

    # -------------------------------------------------------------------------
    # request handlers - per payload
    # -------------------------------------------------------------------------

    def handle_request(self, form_data):
        rqst = self.request(form_data)

        self.log.info("PAYLOAD>> {}\n".format(json.dumps(rqst.payload, indent=3)))
        p_type = rqst.payload['type']
        callback = self._in_msg.listeners(p_type)[0]

        return callback(rqst)

    # -------------------------------------------------------------------------
    # PRIVATE request handlers - per payload type
    # -------------------------------------------------------------------------

    def _handle_block_actions(self, rqst):
        action = rqst.payload['actions'][0]
        value = ui.BLOCKS.v_action(action)
        event = action['block_id']
        callback = self.ux_block.listeners(event)[0]

        return callback(rqst, action, value)

    def _handle_dialog_submit(self, rqst):
        event = rqst.payload['callback_id']
        submission = rqst.payload['submission']
        callback = self.ux_dialog.listeners(event)[0]

        return callback(rqst, submission)

    def _handle_imsg(self, rqst):
        event = rqst.payload['callback_id']
        action_data = rqst.payload['actions'][0]
        action_id, action_value = ui.IMSG.v_action(action_data)
        callback = self.ux_imsg.listeners(event)[0]

        action = ui.IMSG.SlackOnImsgAction(action_data, action_id, action_value)
        return callback(rqst, action)

    def error(self, exc):
        import pdb
        pdb.set_trace()

        if exc.args:
            self.log.error("SlackApp ERROR>>\n{}\n".format(
                json.dumps(exc.args[1])))

        raise exc
