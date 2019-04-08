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

