
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
