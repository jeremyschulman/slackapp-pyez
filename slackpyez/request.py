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
from flask import session

from slackpyez.dialog import SlackDialog
from slackclient import SlackClient
from slackpyez.response import SlackResponse


class SlackRequest(object):

    def __init__(self, app, rqst_data):
        self.app = app
        self.rqst_data = rqst_data

        self.user_id = session['user_id']
        self.payload = session['payload']

        if 'event' in self.rqst_data:
            self.event = self.rqst_data['event']
            # self.user_id = self.event['user']
            self.channel = self.event['channel']
            self.text = self.event['text']
            self.ts = self.event['ts']

        elif 'payload' in self.rqst_data:
            # self.payload = session['payload'] # json.loads(rqst_data['payload'])
            self.channel = self.payload['channel']['id']
            # self.user_id = self.payload['user']['id']
            self.user_name = self.payload['user']['name']
            self.response_url = self.payload['response_url']
            self.trigger_id = self.payload.get('trigger_id')
            self.state = json.loads(self.payload.get('state') or '{}')

        elif 'command' in self.rqst_data:
            self.channel = self.rqst_data["channel_id"]
            # self.user_id = self.rqst_data['user_id']
            self.user_name = self.rqst_data['user_name']
            self.response_url = self.rqst_data['response_url']
            self.trigger_id = self.rqst_data['trigger_id']
        else:
            raise RuntimeError("What is this request?")

        chan_config = app.config.channels[self.channel]
        token = chan_config.get('bot_oauth_token')
        self.bot = bool(token)
        if not self.bot:
            token = chan_config['oauth_token']

        self.client = SlackClient(token=token)

    def delete(self):
        self.response().send(delete_original=True, replace_original=True)

    def dialog(self, **kwargs):
        return SlackDialog(rqst=self, **kwargs)

    def response(self):
        return SlackResponse(rqst=self)
