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
from requests import Session
from . import ux_blocks


__all__ = ['SlackResponse']


class SlackResponse(dict):

    def __init__(self, rqst):
        super(SlackResponse, self).__init__()
        self.app = rqst.app
        self.rqst = rqst
        self.client = rqst.client
        self['as_user'] = self.rqst.bot
        self.request = Session()
        self.request.headers["Content-Type"] = "application/json"
        self.request.verify = False

    # -------------------------------------------------------------------------
    # messaging methods
    # -------------------------------------------------------------------------

    def send_public(self, **kwargs):
        resp = self.client.api_call("chat.postMessage",
                                    channel=self.rqst.channel,
                                    **self, **kwargs)

        self.validate_api_response(resp)

    def send_ephemeral(self, **kwargs):
        api_resp = self.client.api_call("chat.postEphemeral",
                                        user=self.rqst.user_id,
                                        channel=self.rqst.channel,
                                        **self, **kwargs)

        self.validate_api_response(api_resp)

    def send(self, *vargs, **kwargs):
        """
        Send the message to the response_url.  The caller is expected to setup the
        response dictionary items before calling.

        As a 'shortcut feature', if the caller passes a text string as vargs[0],
        then this function will wrap that text in a section block and auto-creates
        the 'blocks' body.  If you use this, do *not* have blocks defined in your
        response message as it will cause a conflict, and you will get a code
        Exception.

        Parameters
        ----------
        vargs : list[<str>][0]
            As described above

        kwargs
            Any additional message body fields to send that are not already
            part of the response dict.

        Raises
        ------
        RuntimeError
            If the call to the Slack API fails.
        """
        if vargs:
            self['blocks'] = [ux_blocks.section(vargs[0])]

        resp = self.request.post(self.rqst.response_url,
                                 json=dict(**self, **kwargs))
        if not resp.ok:
            raise RuntimeError(f"Unable to send response: {resp.text}", resp)

    # -------------------------------------------------------------------------
    # "on" registers
    # -------------------------------------------------------------------------
    # TODO: v---- depreciate this use

    def on_action(self, key, func):
        self.app.register_block_action(key, func)

    @staticmethod
    def validate_api_response(api_resp):
        if api_resp.get("ok"):
            return

        print("API failed, messages: ")
        meta = api_resp.get("response_metadata") or {}
        meta_msgs = meta.get("messages")
        if meta_msgs:
            for message in meta_msgs:
                print(f">: {message}")

        raise RuntimeError(f"Slack API failed.\n{json.dumps(api_resp, indent=3)}\n",
                           api_resp)
