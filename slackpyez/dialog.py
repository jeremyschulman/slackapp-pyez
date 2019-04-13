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


class SlackDialog(dict):

    def __init__(self, rqst, callback_id, on_submit, **_kwargs):
        super(SlackDialog, self).__init__()
        self.rqst = rqst
        self.client = rqst.client
        self.callback_id = callback_id
        self._on_submit_func = None
        self.on_submit = on_submit
        self['state'] = rqst.state
        self.trigger_id = rqst.trigger_id



    def send(self, **kwargs):

        self['state'] = json.dumps(self['state'])
        dialog = dict(callback_id=self.callback_id, **self, **kwargs)

        resp = self.client.api_call(
            "dialog.open", trigger_id=self.trigger_id, dialog=dialog)

        self.rqst.app.validate_api_response(resp)
