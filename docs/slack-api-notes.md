About Slack slash commands
--------------------------
The User will have a number of Slack /<commands> defined, and in each case the request data
that is presented to the handler will have the following format:

request.form ==>
```json
{
   "token": "<>",
   "team_id": "THRDXJR39",
   "team_domain": "nwkautomaniac",
   "channel_id": "CHQQWM6QM",
   "channel_name": "networkautomation",
   "user_id": "UHQ9S2KK6",
   "user_name": "nwkautomaniac",
   "command": "/ngrok",
   "text": "",
   "response_url": "https://hooks.slack.com/commands/<>",
   "trigger_id": "588706891586.603473637111.53d620d700808469f56fb22ce92fac47"
}
```


Slack Dialog Submit
-------------------
````json
{
   "type": "dialog_submission",
   "token": "<>",
   "action_ts": "1554726325.431830",
   "team": {
      "id": "THRDXJR39",
      "domain": "nwkautomaniac"
   },
   "user": {
      "id": "UHQ9S2KK6",
      "name": "nwkautomaniac"
   },
   "channel": {
      "id": "CHQQWM6QM",
      "name": "networkautomation"
   },
   "submission": {
      "location": "School",
      "hostname": "closet-switch1",
   },
   "callback_id": "get-vlans-dialog",
   "response_url": "https://hooks.slack.com/app/<>",
   "state": ""
}
````

Slack Event Data
----------------
request.json ==>
````json
    {
       "token": "<>",
       "team_id": "THRDXJR39",
       "api_app_id": "AHAKQUBNE",
       "event": {
          "client_msg_id": "c71a3f26-3bfb-4b51-b135-b39eb57202d4",
          "type": "app_mention",
          "text": "<@UHGHTPUKT> - are you there?",
          "user": "UHQ9S2KK6",
          "ts": "1554724486.026900",
          "channel": "CHQQWM6QM",
          "event_ts": "1554724486.026900"
       },
       "type": "event_callback",
       "event_id": "EvHBDDH659",
       "event_time": 1554724486,
       "authed_users": [
          "UHGHTPUKT"
       ]
    }
````