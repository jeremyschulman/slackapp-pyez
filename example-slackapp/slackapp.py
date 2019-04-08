from flask import request
from blueprint import blueprint
from slackpyez.slack import SlackApp

slackapp = SlackApp()


@blueprint.route('/slackbot/request', methods=["POST"])
def on_slack_request():
    return slackapp.handle_request(request.form)

