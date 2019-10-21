#  Copyright 2019 Jeremy Schulman, nwkautomaniac@gmail.com
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#  http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from flask import request

from blueprint import blueprint
from app_data import slackapp
from slackpyez.ui import BLOCKS


@blueprint.route("/ngrok", methods=["POST"])
def slackcmd_verify_ngrok():
    rqst = slackapp.request(request.form)
    resp = rqst.response()

    block_id = 'ngrok.button'

    resp['blocks'] = [
        BLOCKS.section('Hi There!'),
        BLOCKS.section(f'You are <@{rqst.user_id}>'),
        BLOCKS.divider(),
        BLOCKS.actions(
            block_id=block_id,
            elements=[
                BLOCKS.e_button('Press for Good',
                                action_id=f'{block_id}.good',
                                value='good'),
                BLOCKS.e_button('Press for Bad',
                                action_id=f'{block_id}.bad',
                                value='bad')
            ]
        ),
        BLOCKS.divider()
    ]

    @slackapp.ui_block.on(block_id)
    def _on_button(rqst, action, value):
        """ this function will be called when the User clicks on the of buttons defined """
        resp = rqst.response()
        resp.send(f"at time {action['action_ts']}, you pressed: {value}")
        return ''

    resp.send().raise_for_status()
    return ''

