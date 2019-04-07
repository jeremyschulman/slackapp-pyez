About Slack slash commands
--------------------------
The User will have a number of Slack /<commands> defined, and in each case the request data
that is presented to the handler will have the following format:

request.form ==>
    {
       "token": "<#SECRET#>",
       "team_id": "THRDXJR39",
       "team_domain": "nwkautomaniac",
       "channel_id": "CHQQWM6QM",
       "channel_name": "networkautomation",
       "user_id": "UHQ9S2KK6",
       "user_name": "nwkautomaniac",
       "command": "/ngrok",
       "text": "",
       "response_url": "https://hooks.slack.com/commands/THRDXJR39/600121632864/SJD0LXtSuhMbJr4To7zXrETQ",
       "trigger_id": "588706891586.603473637111.53d620d700808469f56fb22ce92fac47"
    }
