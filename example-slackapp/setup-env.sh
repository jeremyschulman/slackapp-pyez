# the flaskapp-env.sh contains environment variables that are passed into the
# app for Flask specific controls.

export FLASKAPP_SETTINGS=$(PWD)/flaskapp-env.sh

# the slackapp.toml file is not stored in the repo since it contains tokens.
# See the file "slackapp-template.toml" for details on creating your own file.

export SLACKAPP_SETTINGS=$(PWD)/../../slackapp.toml
