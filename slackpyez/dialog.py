
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
