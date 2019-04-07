import os
import json
from pathlib import Path

from flask import request, jsonify
import toml

from slackpyez.callback_handler import CallbackHandler
from slackpyez.request import SlackRequest


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


class SlackApp(object):

    def __init__(self):
        self.on_block_actions = CallbackHandler(('block_id', 'action_id'))
        self.on_dialog_submit = CallbackHandler('callback_id')
        self.on_payload_type = CallbackHandler('type')

        self.config = SlackAppConfig()

        # setup the default handler functions

        self.on_payload_type['block_actions'] = self.handle_block_actions
        self.on_payload_type['dialog_submission'] = self.handle_dialog_submit

    # def register_block_actions(self, on_defs):
    #     for key_val, func in on_defs:
    #         self.on_block_actions[key_val] = func

    def register_block_action(self, key, func):
        self.on_block_actions[key] = func

    def register_dialog_submit(self, callback_id, func):
        self.on_dialog_submit[callback_id] = func

    def request(self, rqst_form):
        return SlackRequest(app=self, form_data=rqst_form)

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

    # -------------------------------------------------------------------------
    # request handlers
    # -------------------------------------------------------------------------

    def handle_block_actions(self, payload, rqst):
        action = payload['actions'][0]
        return self.on_block_actions(action=action, payload=payload, rqst=rqst)

    def handle_dialog_submit(self, payload, rqst):
        return self.on_dialog_submit(payload=payload, submit=payload['submission'], rqst=rqst)

    def handle_request(self, form_data):
        rqst = self.request(form_data)

        form_data = {k:v for k, v in request.form.items() if k != 'payload'}
        print("FORM>> {}".format(json.dumps(form_data, indent=3)))
        print("PAYLOAD>> {}\n".format(json.dumps(rqst.payload, indent=3)))

        rv = self.on_payload_type(rqst.payload, rqst)
        return jsonify(rv) if rv else ""
