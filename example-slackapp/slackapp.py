import json
from flask import request, jsonify

from blueprint import blueprint
from slackpyez.slack import SlackApp

slackapp = SlackApp()


@slackapp.on_payload_type.handle('block_actions')
def slackrqst_bloack_actions(payload, rqst):
    action = payload['actions'][0]
    return slackapp.on_block_actions(action, payload=payload, rqst=rqst)


@slackapp.on_payload_type.handle('dialog_submission')
def slackrqst_dialog_submit(payload, rqst):
    return slackapp.on_dialog_submit(
        payload, submit=payload['submission'], rqst=rqst)


@blueprint.route('/slackbot/request', methods=["POST"])
def api_slackbot_request():

    rqst = slackapp.request(request.form)

    form_data = {k:v for k,v in request.form.items() if k != 'payload'}
    print("FORM>> {}".format(json.dumps(form_data, indent=3)))
    print("PAYLOAD>> {}\n".format(json.dumps(rqst.payload, indent=3)))

    rv = slackapp.on_payload_type(rqst.payload, rqst)
    return jsonify(rv) if rv else ""

