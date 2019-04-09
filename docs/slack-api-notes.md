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


Slack Action Request
--------------------
````json
{
   "type": "block_actions",
   "team": {
      "id": "THRDXJR39",
      "domain": "nwkautomaniac"
   },
   "user": {
      "id": "UHQ9S2KK6",
      "username": "nwkautomaniac",
      "name": "nwkautomaniac",
      "team_id": "THRDXJR39"
   },
   "api_app_id": "AHAKQUBNE",
   "token": "<>",
   "container": {
      "type": "message",
      "message_ts": "1554741985.040800",
      "channel_id": "CHQQWM6QM",
      "is_ephemeral": true
   },
   "trigger_id": "589903540066.603473637111.b2931cc1a88394ca1b3e04c5c0c176e7",
   "channel": {
      "id": "CHQQWM6QM",
      "name": "networkautomation"
   },
   "response_url": "https://hooks.slack.com/actions/<>",
   "actions": [
      {
         "type": "static_select",
         "action_id": "net_command_id",
         "block_id": "net_command",
         "selected_option": {
            "text": {
               "type": "plain_text",
               "text": "Bounce Port",
               "emoji": true
            },
            "value": "net-bounce-port"
         },
         "placeholder": {
            "type": "plain_text",
            "text": "Get VLANS",
            "emoji": true
         },
         "action_ts": "1554741987.604084"
      }
   ]
}
````
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


Interactive Message Response
----------------------------
```json
{
   "type": "interactive_message",
   "actions": [
      {
         "name": "go_button",
         "type": "button",
         "value": "yes"
      }
   ],
   "callback_id": "get-vlans-callback",
   "team": {
      "id": "THRDXJR39",
      "domain": "nwkautomaniac"
   },
   "channel": {
      "id": "CHQQWM6QM",
      "name": "networkautomation"
   },
   "user": {
      "id": "UHQ9S2KK6",
      "name": "nwkautomaniac"
   },
   "action_ts": "1554829380.182062",
   "message_ts": "1554829376.086100",
   "attachment_id": "1",
   "token": "<>",
   "is_app_unfurl": false,
   "response_url": "https://hooks.slack.com/actions/<>",
   "trigger_id": "606070084439.603473637111.48d20eb731dee79797d61bdcc10938d6"
}
 ```
