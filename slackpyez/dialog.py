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
from slackpyez.slackapi import SlackApiResponse
import slackpyez.ui_dialog as ui


class SlackDialog(UserDict):

    def __init__(self, rqst):
        super(SlackDialog, self).__init__()
        self.rqst = rqst
        self.app = rqst.app
        self.client = rqst.client
        self.trigger_id = rqst.trigger_id

    @property
    def ui(self):
        """ convenience to the module containing the UI widgets """
        return ui

    @property
    def event(self):
        """ get/set the callback_id within the dialog body """
        return self.get('callback_id')

    @event.setter
    def event(self, callback_id):
        self['callback_id'] = callback_id

    def on(self, event):
        """
        Convenience decorator that will assign the event into the dialog
        and the return the slack app 'ui_dialog' event emitter.on for
        the purpose of callback registration.

        Examples
        --------
            @dialog.on('my event')
            def sumitted(rqst_from_dialog, submission):
                ... code that handles the data in submission ...

                new_resp = rqst_from_dialog.response()
                ... setup new response to User

                new_response.send().raise_for_status()

        Parameters
        ----------
        event : str
            The event value that will be registered for dialog_submission
            callback_id.

        Returns
        -------
        callable - decorator of slack app
        """
        self.event = event
        return self.app.ui_dialog.on(event)

    def send(self, **kwargs):
        if not self.event:
            raise RuntimeError("Missing required event callback_id")

        return SlackApiResponse(self.rqst, self.client.api_call(
            "dialog.open",
            trigger_id=self.trigger_id,
            dialog=dict(**self, **kwargs)
        ))
