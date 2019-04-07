import json
from slackpyez.dialog import SlackDialog
from requests import Session
from slackclient import SlackClient

from slackpyez.response import SlackResponse


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

    @staticmethod
    def delete(rt='ephemeral'):
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

    def dialog(self, **kwargs):
        return SlackDialog(rqst=self, **kwargs)

    def response(self):
        return SlackResponse(rqst=self)
