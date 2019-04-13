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

from requests import Session
from collections import UserDict

from slackpyez import ui_blocks
from slackpyez.slackapi import SlackApiResponse, SlackApiPostResponse


__all__ = ['SlackResponse']


class SlackResponse(UserDict):

    def __init__(self, rqst):
        super(SlackResponse, self).__init__()
        self.app = rqst.app
        self.rqst = rqst
        self.client = rqst.client

        self.request = Session()
        self.request.headers["Content-Type"] = "application/json"
        self.request.verify = False

    # -------------------------------------------------------------------------
    # messaging methods
    # -------------------------------------------------------------------------

    def wrap_text(self, text):
        blocks = self.get('blocks') or []
        blocks.insert(0, ui_blocks.section(text))
        self['blocks'] = blocks

    def send_public(self, text=None, **kwargs):
        """
        Send the response to the channel so that all Users will see this
        message.

        Other Parameters
        ----------------
        Any additional message body parameters not already set in the response
        object.

        Raises
        ------
        SlackAppApiError
            Upon failure sending message to Slack API
        """
        if text:
            self.wrap_text(text)

        resp = self.client.api_call("chat.postMessage",
                                    channel=self.rqst.channel,
                                    **self, **kwargs)

        return SlackApiResponse(self, resp)

    def send_ephemeral(self, text=None, user_id=None, **kwargs):
        """
        Send an ephemeral message to the User in the channel that received the
        request.

        Alternatively the caller can send the ephMsg to a different user if the
        `user_id` is provided.

        Parameters
        ----------
        text : str (optional)
            If provided this text will be added as the first block in the
            message.

        user_id : str (optional)
            The user to receive the ephMsg

        Other Parameters
        ----------------
        Any additional message body parameters not already set in the response
        object.

        Raises
        ------
        SlackAppApiError
            Upon failure sending message to Slack API
        """
        if text:
            self.wrap_text(text)

        api_resp = self.client.api_call("chat.postEphemeral",
                                        user=(user_id or self.rqst.user_id),
                                        channel=self.rqst.channel,
                                        **self, **kwargs)

        return SlackApiResponse(self, api_resp)

    def send(self, text=None, **kwargs):
        """
        Send the message to the response_url, which will replace the originating
        message.

        As a 'shortcut feature', if the caller passes `text` parameter then this
        function will wrap that text in a section block and auto-creates the
        'blocks' body.

        Notes
        -----
        API: https://api.slack.com/interactive-messages

        Parameters
        ----------
        text : str (optional) - as described above

        Other Parameters
        ----------------
        Any additional message body parameters not already set in the response
        object.

        Raises
        ------
        SlackAppApiError
            Upon failure sending message to Slack API
        """
        if text:
            self.wrap_text(text)

        resp = self.request.post(self.rqst.response_url,
                                 json=dict(**self, **kwargs))

        return SlackApiPostResponse(self, resp)

    def send_dm(self, channel, **kwargs):
        resp = self.client.api_call("chat.postMessage",
                                    channel=channel,
                                    **self, **kwargs)

        return SlackApiResponse(self, resp)
