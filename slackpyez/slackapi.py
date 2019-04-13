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

from . import exc


class SlackApiResponse(object):
    def __init__(self, rqst, resp):
        self.rqst = rqst
        self.app = rqst.app
        self.resp = resp

    @property
    def ok(self):
        return self.resp.get('ok', False) is True

    def raise_for_status(self):
        if self.ok:
            return

        self.app.error(exc.SlackAppApiError(self))


class SlackApiPostResponse(SlackApiResponse):
    @property
    def ok(self):
        return self.resp.ok
