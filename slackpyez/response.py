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

__all__ = ['SlackResponse']


class SlackResponse(dict):

    DEFAULT_SELECT_PLACEHOLDER = '-select-'

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
    # b_<item> - build blocks for slack messaging
    # -------------------------------------------------------------------------

    @staticmethod
    def b_section(text, **kwargs):
        return {'type': 'section',
                'text': SlackResponse.c_text(text),
                **kwargs}

    @staticmethod
    def b_context(elements):
        return {
            'type': 'context',
            'elements': elements
        }

    @staticmethod
    def b_divider():
        return {'type': 'divider'}

    @staticmethod
    def b_actions(elements, **kwargs):
        return {'type': 'actions',
                'elements': elements,
                **kwargs}

    @staticmethod
    def b_image(image_url, alt_text, **kwargs):
        """

        Other Parameters
        ----------------
        title : text object
        block_id : str
        """
        return {
            'type': 'image',
            'image_url': image_url,
            'alt_text': alt_text,
            **kwargs
        }

    # -------------------------------------------------------------------------
    # e_<item> - block element definitions
    # -------------------------------------------------------------------------

    @staticmethod
    def e_button(text, action_id=None, **kwargs):
        return {
            'type': 'button',
            'text': SlackResponse.c_text(text, ttype='plain_text'),
            'action_id': action_id or text,
            **kwargs}

    @staticmethod
    def e_image(image_url, alt_text):
        return {
            'type': 'image',
            'image_url': image_url,
            'alt_text': alt_text
        }

    @staticmethod
    def e_static_select(action_id, placeholder=None,
                        options=None, option_groups=None,
                        **kwargs):
        """
        This helper creates the "menu option select" message element dictionary.

        Parameters
        ----------
        action_id
        placeholder
        options
        option_groups
        kwargs

        Other Parameters
        ----------------

        Returns
        -------
        dict
        """
        ele = {
            'type': 'static_select',
            'action_id': action_id,
            'placeholder': SlackResponse.c_text(
                placeholder or SlackResponse.DEFAULT_SELECT_PLACEHOLDER,
                'plain_text')
        }

        if options:
            ele['options'] = options
        elif option_groups:
            ele['option_groups'] = option_groups

        else:
            raise RuntimeError("Missing arg 'options' | 'option_groups'")

        ele.update(kwargs)
        return ele

    # -------------------------------------------------------------------------
    # c_<item> - message composition object
    # -------------------------------------------------------------------------

    @staticmethod
    def c_text(text, ttype='mrkdwn'):
        return {'type': ttype, 'text': text}

    @staticmethod
    def c_option(text, value):
        return {'text': SlackResponse.c_text(text, 'plain_text'),
                'value': value}

    @staticmethod
    def c_option_group(label, options):
        return {
            'label': SlackResponse.c_text(label, 'plain_text'),
            'options': [
                SlackResponse.c_option(label, value)
                for label, value in options
            ]
        }

    @staticmethod
    def c_confirm(title, text, confirm, deny='Cancel'):
        return {
            'title': SlackResponse.c_text(title, 'plain_text'),
            'text': SlackResponse.c_text(text),
            'confirm': SlackResponse.c_text(confirm, 'plain_text'),
            'deny': SlackResponse.c_text(deny, 'plain_text')
        }

    # -------------------------------------------------------------------------
    # v_<item> - get value helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def v_action_selected(action):
        return action['selected_option']['value']

    @staticmethod
    def v_first_option(options):
        return options[0]['text']['text']

    @staticmethod
    def v_first_group_option(group_options):
        return group_options[0]['options'][0]['text']['text']

    # -------------------------------------------------------------------------
    # messaging methods
    # -------------------------------------------------------------------------

    def send_public(self, **kwargs):
        resp = self.client.api_call(
            "chat.postMessage", channel=self.rqst.channel,
            **self, **kwargs)

        self.rqst.app.validate_api_response(resp)

    def send_ephemeral(self, **kwargs):
        api_resp = self.client.api_call(
            "chat.postEphemeral", user=self.rqst.user_id, channel=self.rqst.channel,
            **self, **kwargs)

        self.rqst.app.validate_api_response(api_resp)

    def on_action(self, key, func):
        self.app.register_block_action(key, func)

    def send(self, *vargs, **kwargs):
        if vargs:
            self['blocks'] = [self.b_section(vargs[0])]

        resp = self.request.post(self.rqst.response_url,
                                 json=dict(**self, **kwargs))
        if not resp.ok:
            raise RuntimeError(f"Unable to send response: {resp.text}", resp)
