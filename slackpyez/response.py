
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
        return {'type': 'actions',
                'elements': elements,
                **kwargs}

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

    @staticmethod
    def e_image(image_url, alt_text):
        return {
            'type': 'image',
            'image_url': image_url,
            'alt_text': alt_text
        }

    @staticmethod
    def e_static_select(placeholder, action_id, options=None, option_groups=None, **kwargs):
        ele = {
            'type': 'static_select',
            'placeholder': SlackResponse.c_text(placeholder, 'plain_text'),
            'action_id': action_id,
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

    def on_action(self, key, func):
        self.app.register_block_action(key, func)

    def send(self, *vargs, **kwargs):
        if vargs:
            self['blocks'] = [self.b_section(vargs[0])]

        resp = self.rqst.request.post(self.rqst.response_url,
                                      json=dict(**self, **kwargs))
        if not resp.ok:
            raise RuntimeError(f"Unable to send response: {resp.text}", resp)
