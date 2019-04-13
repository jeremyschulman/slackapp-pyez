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

from collections import UserDict


from slackpyez import ux_dialog
from slackpyez.slackapi import SlackApiResponse


class SlackDialog(UserDict):

    def __init__(self, rqst):
        super(SlackDialog, self).__init__()
        self.rqst = rqst
        self.app = rqst.app
        self.client = rqst.client

        self.trigger_id = rqst.trigger_id
        self.ux = ux_dialog
        self.callback_id = None

    def on(self, callback_id, func):
        self.callback_id = callback_id
        self.app.ux_dialog.on(callback_id, func)

    def send(self, **kwargs):
        # self['state'] = json.dumps(self['state'])

        if not self.callback_id:
            raise RuntimeError("Missing required callback_id")

        resp = self.client.api_call(
            "dialog.open",
            trigger_id=self.trigger_id,
            callback_id=self.callback_id,
            **self, **kwargs)

        return SlackApiResponse(rqst=self, resp=resp)
