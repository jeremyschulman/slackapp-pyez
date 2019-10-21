# Example Slack-PyEz App

This directory contains a basic working slack app.  Before you begin working
with this app, you should be familiar with setting up the Slack API aspects on
[api.slack.com](https://api.slack.com).  

In order for you app to connect with Slack, your app must be reachable by the
Slack API system.  You can use the program [ngrok](https://ngrok.com/) for this purpose,
as described in this [article](https://api.slack.com/tutorials/tunneling-with-ngrok).

# Before you begin

Once you've created you API there, you will need to create a file called
`slackapp.toml` that contains the various tokens needed to exchange data
between your app and the Slack API system.  See the file
[slackapp-template.toml](slackapp-template.toml) for further details.  You then
must edit the file [setup-env.sh](setup-env.sh) to change the
`SLACKAPI_SETTINGS` variable to point to the file on your local system. 
Generally speaking, you should *NOT* store the slackapp.toml file in your
repository if you plan to checkin your code; so you will see that the
`SLACKAPI_SETTINGS` variable points to a file outside the current project
directory structure.

You must then source the `setup-env.sh` file to load the variables into your
environment:

```shell script
$ source setup-env.sh
```

If you want to change the Flask app port used for this demonstration, you can
edit the file [flaskapp-env.sh](flaskapp-env.sh) and change the `PORT` value. 
You do not need to source this file as it is automatically loaded by the
slackpyez framework.

# Running the example

Once you have everything configured and setup properly, you can start the example 
application:

```shell script
$ python run.py
```

You should see output similar to this:

```shell script
/api/v1/slack/request
/api/v1/ngrok
/slack/event
/api/v1/static/<path:filename>
/static/<path:filename>
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://localhost:9000/ (Press CTRL+C to quit)
 * Restarting with stat
/api/v1/slack/request
/api/v1/ngrok
/slack/event
/api/v1/static/<path:filename>
/static/<path:filename>
 * Debugger is active!
 * Debugger PIN: 213-319-504
```

You can then go to your Slack client and issue the "/ngrok" command.  You
should see a response that says "Hi There!  You are <your-user name>!" and then
two buttons.  You can press a button and see the response.  The code for pressing the "/ngrok"
command can be found in the [api_ngrok.py](api/api_ngrok.py) file.

Good luck and have fun!
