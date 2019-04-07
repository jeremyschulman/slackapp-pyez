import os
import json
import toml
from pathlib import Path

from requests import Session
from slackclient import SlackClient

from slackpyez.callback_handler import CallbackHandler


class SlackAppConfig(dict):
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

        slack_api_config = toml.load(conf_file_p)

        self.channels = {_chan['id']: _chan
                         for _chan in slack_api_config['channel']}

        self['ALL_SLACK_VERIFY_TOKENS'] = [
            _chan['verify_token']
            for _chan in slack_api_config['channel']
        ]

        self['SLACK_CHANNEL_NAME_TO_ID'] = {
            _chan['name']: _chan['id']
            for _chan in slack_api_config['channel']
        }


class SlackDialog(object):
    def __init__(self, rqst, callback_id):
        self.callback_id = callback_id
        self.rqst = rqst
        self.client = rqst.client

    @staticmethod
    def i_option(label, value):
        return dict(label=label, value=value)

    @staticmethod
    def e_text(label, name, **kwargs):
        return {'type': 'text', 'label': label, 'name': name,
                **kwargs}

    @staticmethod
    def e_select(label, name, **kwargs):
        return {'type': 'select', 'label': label, 'name': name, **kwargs}

    def send(self, title, **kwargs):
        dialog = dict(title=title, callback_id=self.callback_id, **kwargs)

        response_json = self.client.api_call(
            "dialog.open", trigger_id=self.rqst.trigger_id, dialog=dialog)

        self.rqst.app.validate_api_response(response_json, "dialog.open")


class SlackResponse(dict):

    def __init__(self, rqst):
        super(SlackResponse, self).__init__()
        self.app = rqst.app
        self.rqst = rqst
        self.client = rqst.client

    # -------------------------------------------------------------------------
    # b_<item> - build blocks for slack messaging
    # -------------------------------------------------------------------------

    @staticmethod
    def b_section(text, **kwargs):
        return {'type': 'section',
                'text': SlackResponse.c_text(text),
                **kwargs}

    @staticmethod
    def b_divider():
        return {'type': 'divider'}

    @staticmethod
    def b_actions(elements, **kwargs):
        return {'type': 'actions', 'elements': elements, **kwargs}

    # -------------------------------------------------------------------------
    # e_<item> - block element definitions
    # -------------------------------------------------------------------------

    @staticmethod
    def e_button(text, **kwargs):
        return {
            'type': 'button',
            'text': SlackResponse.c_text(text, ttype='plain_text'),
            'action_id': kwargs.get('action_id') or text,
            **kwargs}

    # -------------------------------------------------------------------------
    # c_<item> - message composition object
    # -------------------------------------------------------------------------

    @staticmethod
    def c_text(text, ttype='mrkdwn'):
        return {'type': ttype, 'text': text}

    # -------------------------------------------------------------------------
    # messaging methods
    # -------------------------------------------------------------------------

    def send_message(self, **kwargs):
        response_json = self.client.api_call("chat.postMessage",
                                             channel=self.rqst.channel, **kwargs)

        self.rqst.app.validate_api_response(response_json, "chat.postMessage")

    def send_ephemeral_message(self, **kwargs):
        response_json = self.client.api_call(
            "chat.postEphemeral", user=self.rqst.user_id, channel=self.rqst.channel,
            **kwargs
        )
        self.rqst.app.validate_api_response(response_json, "chat.postEphemeral")

    def send(self, *vargs, _on_actions=None):
        if vargs:
            self['blocks'] = [self.b_section(vargs[0])]

        if _on_actions:
            self.app.register_block_actions(_on_actions)

        resp = self.rqst.request.post(self.rqst.response_url,
                                      json=dict(**self))
        if not resp.ok:
            raise RuntimeError(f"Unable to send response: {resp.text}", resp)


class SlackRequest(object):

    def __init__(self, app, form_data):
        self.app = app
        self.form = form_data
        self.payload = json.loads(form_data.get('payload') or '{}')
        self.channel = form_data.get('channel_id') or self.payload['channel']['id']

        self.user_id = form_data.get('user_id') or self.payload['user']['id']
        self.user_name = form_data.get('user_name') or self.payload['user']['name']

        self.response_url = self.form.get('response_url') or self.payload.get('response_url')
        self.trigger_id = self.form.get('trigger_id') or self.payload.get('trigger_id')

        oauth_token = app.config.channels[self.channel]['oauth_token']
        self.client = SlackClient(token=oauth_token)

        self.request = Session()
        self.request.headers["Content-Type"] = "application/json"
        self.request.verify = False

    def delete(self, rt='ephemeral'):
        return {
            'response_type': rt,
            'text': '',
            'replace_original': True,
            'delete_original': True
        }

    #
    # # -------------------------------------------------------------------------
    # # m_<item> - build dicts used for slack messaging data structures
    # # -------------------------------------------------------------------------
    #
    # @staticmethod
    # def m_text(text, ttype='mrkdwn'):
    #     return {'type': ttype, 'text': text}
    #
    # @staticmethod
    # def m_image(image_url, alt_text=None):
    #     return {"type": "image", "image_url": image_url,
    #             "alt_text": alt_text or image_url.rpartition('/')[-1]}
    #
    # @staticmethod
    # def m_option(text, value):
    #     return {'text': Slack.m_text(text, ttype='plain_text'),
    #             'value': value}

    # # -------------------------------------------------------------------------
    # # e_<item> - build dicts used for slack block elements
    # # -------------------------------------------------------------------------
    #
    # @staticmethod
    # def e_button(text, **kwargs):
    #     return {
    #         'type': 'button',
    #         'text': Slack.m_text(text, ttype='plain_text'),
    #         'action_id': kwargs.get('action_id') or text,
    #         **kwargs
    #     }
    #
    # @staticmethod
    # def e_static_select(name, **kwargs):
    #     return {
    #         'type': 'static_select',
    #         'placeholder': Slack.m_text(name, ttype='plain_text'),
    #         'action_id': kwargs.get('action_id') or name,
    #         **kwargs
    #     }

    def dialog(self, callback_id):
        return SlackDialog(rqst=self, callback_id=callback_id)

    def response(self):
        return SlackResponse(rqst=self)


class SlackApp(object):

    def __init__(self):
        self.on_block_actions = CallbackHandler(('block_id', 'action_id'))
        self.on_dialog_submit = CallbackHandler('callback_id')
        self.on_payload_type = CallbackHandler('type')

        self.handler_for_type = dict(
            block_actions=self.on_block_actions,
            dialog_submission=self.on_dialog_submit)

        self.config = SlackAppConfig()

    def register_block_actions(self, on_defs):
        for key_val, func in on_defs:
            self.on_block_actions[key_val] = func

    def request(self, rqst_form):
        return SlackRequest(app=self, form_data=rqst_form)

    @staticmethod
    def validate_api_response(response_json, api_method):
        if not response_json.get("ok"):
            print(f"An error occurred while executing {api_method}")
            meta = response_json.get("response_metadata") or {}
            meta_msgs = meta.get("messages")
            if meta_msgs:
                for message in meta_msgs:
                    print(f"Response Metadata Message: {message}")

            print(f"Full json response: {response_json}")
