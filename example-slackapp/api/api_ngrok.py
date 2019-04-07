from flask import request

from blueprint import blueprint
from slackapp import slackapp


@blueprint.route("/ngrok", methods=["POST"])
def slackcmd_verify_ngrok():

    rqst = slackapp.request(request.form)
    resp = rqst.response()

    resp['blocks'] = [
        resp.b_section('Hi There!'),
        resp.b_section(f'You are <@{rqst.user_id}>'),
        resp.b_divider(),
        resp.b_actions(block_id='ngrok', elements=[
            resp.e_button('Good'),
            resp.e_button('Bad')
        ]),
        resp.b_divider()
    ]

    resp.send(_on_actions=[(('ngrok', 'Good'), _on_button),
                           (('ngrok', 'Bad'), _on_button)])

    return ""


def _on_button(action, rqst, **_kwargs):
    action_id = action['action_id']
    resp = rqst.response()
    resp.send(f'You pressed >>{action_id}<<')

    # delete the original request since this was a button action.

    return rqst.delete()

