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

"""
This file implements a Flask SessionInterface that will create sessions based on the Slack user_id
value.  If the inbound message is not "slack related", then it will use a standard cookies approach.

Some of this code was inspired from: http://flask.pocoo.org/snippets/132/
"""

import os
from pathlib import Path
from contextlib import suppress
from collections import UserDict

import json
import pickle
from uuid import uuid1
from flask.sessions import SessionInterface, SessionMixin

__all__ = ['SlackAppSessionInterface']


class PickleSession(UserDict, SessionMixin):

    def __init__(self, session_if, sid):
        super(PickleSession, self).__init__()
        self.session_if = session_if
        self.path = session_if.directory / sid
        self.sid = sid
        self.read()

    def read(self):
        try:
            pdata = pickle.load(self.path.open('rb'))
            self.update(pdata)
        except (FileNotFoundError, ValueError, EOFError, pickle.UnpicklingError):
            pass

    def save(self, *vargs, **kwargs):
        with self.path.open('wb') as ofile:
            pickle.dump(self.copy(), ofile)


class PickleSlackSession(PickleSession):

    def save(self, *vargs, **kwargs):
        self.pop('payload', None)                   # do not store payload
        super(PickleSlackSession, self).save()


class PickleCookieSession(PickleSession):

    def __init__(self, session_if, request, app,):
        sid = (request.cookies.get(app.session_cookie_name) or
               '{}-{}'.format(uuid1(), os.getpid()))

        super(PickleCookieSession, self).__init__(session_if, sid)

    def save(self, app, session, response):
        domain = self.session_if.get_cookie_domain(app)

        if not session:
            with suppress(FileNotFoundError):
                session.path.unlink()
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return

        cookie_exp = self.session_if.get_expiration_time(app, session)
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True, domain=domain)


class SlackAppSessionInterface(SessionInterface):

    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)

    def open_session(self, app, request):
        if 'X-Slack-Signature' not in request.headers:
            return PickleCookieSession(self, request, app)

        err = False
        r_form = request.form
        payload = None

        if 'payload' in r_form:
            payload = json.loads(request.form['payload'] or '{}')
            rqst_type = payload['type']
            sid = payload['user']['id']
        elif 'command' in r_form:
            rqst_type = 'command'
            sid = r_form['user_id']
        elif request.json:
            if 'event' in request.json:
                rqst_type = 'event'
                sid = request.json['event']['user']
            elif 'type' in request.json:
                return PickleCookieSession(self, request, app)
            else:
                err = True
        else:
            err = True

        if err:
            print("HEADERS>> {}".format(json.dumps(dict(request.headers), indent=3)))
            print("FORM>> {}".format(json.dumps(r_form, indent=3)))
            print("JSON>> {}".format(json.dumps(request.json, indent=3)))
            raise RuntimeError("Do not know this Slack API.")

        session = PickleSlackSession(self, sid)
        session['rqst_type'] = rqst_type
        session['user_id'] = sid
        session['payload'] = payload
        return session

    def save_session(self, app, session, response):
        session.save(app, session, response)
