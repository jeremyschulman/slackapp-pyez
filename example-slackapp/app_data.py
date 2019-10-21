
import json

from slackeventsapi import SlackEventAdapter
from slackpyez.slackapp import SlackApp


slackapp = SlackApp()
slack_event_adapter = None
flaskapp = None


class MyEventAdapter(SlackEventAdapter):
    def emit(self, event, *args, **kwargs):
        print(f"Event>> {event}")
        print("Body >> {}".format(json.dumps(args[0], indent=3)))
        super(MyEventAdapter, self).emit(event, *args, **kwargs)


def create_event_adapter(flaskapp, secret):
    global slack_event_adapter
    slack_event_adapter = SlackEventAdapter(
        signing_secret=secret,
        endpoint='/slack/event',
        server=flaskapp)


def register_flaskapp(app):
    global flaskapp

    flaskapp = app
    return app
