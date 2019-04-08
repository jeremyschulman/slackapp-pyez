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

import os
import json
from pickle import UnpicklingError, dumps, loads
from flask.sessions import SessionInterface, SessionMixin

__all__ = ['SlackSessionInterface']


class PickleSession(dict, SessionMixin):
    """Server-side session implementation.

    Uses pickle to achieve a disk-backed session such that multiple
    worker processes can access the same session data.
    """

    def __init__(self, directory, sid, *args, **kwargs):
        self.path = os.path.join(directory, sid)
        self.directory = directory
        self.sid = sid
        self.data = None
        self.read()

    def __getitem__(self, key):
        self.read()
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()

    def __delitem__(self, key):
        del self.data[key]
        self.save()

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def read(self):
        """Load pickle from (ram)disk."""
        try:
            with open(self.path, 'rb') as blob:
                self.data = loads(blob.read())
        except (FileNotFoundError, ValueError, EOFError, UnpicklingError):
            self.data = {}

    def save(self):
        """Dump pickle to (ram)disk atomically."""
        new_name = '{}.new'.format(self.path)
        with open(new_name, 'wb') as blob:
            blob.write(dumps(self.data))
        os.rename(new_name, self.path)


class SlackSessionInterface(SessionInterface):
    """Basic SessionInterface which uses the PickleSession."""

    def __init__(self, directory):
        self.directory = os.path.abspath(directory)
        os.makedirs(self.directory, exist_ok=True)

    def open_session(self, app, request):
        r_form = request.form
        sid = (r_form.get('user_id') or
               r_form.get('user') or
               request.json.get('event', {}).get('user'))

        payload = None
        if not sid and 'payload' in request.form:
            payload = json.loads(request.form['payload'] or '{}')
            sid = payload['user']['id']

        session = PickleSession(self.directory, sid)
        session['user_id'] = sid
        session['payload'] = payload
        return session

    def save_session(self, app, session, response):
        session.save()
