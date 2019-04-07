import json

class SlackDialog(dict):

    def __init__(self, rqst, callback_id, on_submit, **_kwargs):
        super(SlackDialog, self).__init__()
        self.rqst = rqst
        self.client = rqst.client
        self.callback_id = callback_id
        self._on_submit_func = None
        self.on_submit = on_submit
        self.state = json.loads(rqst.payload.get('state') or '{}')
        self.trigger_id = rqst.trigger_id

    @property
    def on_submit(self):
        return self._on_submit_func

    @on_submit.setter
    def on_submit(self, func):
        self.rqst.app.register_dialog_submit(self.callback_id, func)

    @staticmethod
    def i_option(label, value):
        return dict(label=label, value=value)

    @staticmethod
    def e_text(label, name, **kwargs):
        return {'type': 'text', 'label': label, 'name': name,
                **kwargs}

    @staticmethod
    def e_select(text, name, options=None, option_groups=None, **kwargs):
        if options:
            kwargs['options'] = options
        elif option_groups:
            kwargs['option_groups'] = option_groups
        else:
            raise RuntimeError("Missing param 'options' or 'option_groups'.")

        return {'type': 'select', 'label': text, 'name': name, **kwargs}

    def send(self, **kwargs):

        dialog = dict(callback_id=self.callback_id, **self, **kwargs)
        dialog['state'] = json.dumps(self.state)

        resp = self.client.api_call(
            "dialog.open", trigger_id=self.trigger_id, dialog=dialog)

        self.rqst.app.validate_api_response(resp)
