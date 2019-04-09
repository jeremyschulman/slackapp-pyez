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

import json
import pickle
from uuid import uuid1
from flask.sessions import SessionInterface, SessionMixin

__all__ = ['SlackSessionInterface']


class PickleSlackSession(dict, SessionMixin):

    def __init__(self, session_if, sid):
        super(PickleSlackSession, self).__init__()
        self.session_if = session_if
        self.path = session_if.directory / sid
        self.sid = sid
        self.read()

    def __getitem__(self, key):
        return super(PickleSlackSession, self).__getitem__(key)

    def __setitem__(self, key, value):
        super(PickleSlackSession, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(PickleSlackSession, self).__delitem__(key)

    def __iter__(self):
        return super(PickleSlackSession, self).__iter__()

    def __len__(self):
        return super(PickleSlackSession, self).__len__()

    def read(self):
        try:
            pdata = pickle.load(self.path.open('rb'))
            dict.update(self, pdata)
        except (FileNotFoundError, ValueError, EOFError, pickle.UnpicklingError):
            pass

    def save(self, *vargs, **kwargs):
        with self.path.open('wb') as ofile:
            pickle.dump(dict.copy(self), ofile)


class PickleCookieSession(PickleSlackSession):

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


class SlackSessionInterface(SessionInterface):

    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)

    def open_session(self, app, request):
        if 'X-Slack-Signature' not in request.headers:
            return PickleCookieSession(self, request, app)

        r_form = request.form
        payload = None

        if 'event' in r_form:
            sid = r_form['user']
        elif 'payload' in r_form:
            payload = json.loads(request.form['payload'] or '{}')
            sid = payload['user']['id']
        elif 'command' in r_form:
            sid = r_form['user_id']
        else:
            raise RuntimeError("Do not know this Slack API.")

        session = PickleSlackSession(self, sid)
        session['user_id'] = sid
        session['payload'] = payload or {}
        return session

    def save_session(self, app, session, response):
        session.save(app, session, response)
