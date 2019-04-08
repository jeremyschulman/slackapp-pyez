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

from collections import Callable
from operator import itemgetter


class CallbackHandler(dict):

    def __init__(self, key):
        super(CallbackHandler, self).__init__()
        if isinstance(key, str):
            get_key = itemgetter(key)
        elif isinstance(key, tuple):
            get_key = itemgetter(*key)
        elif isinstance(key, Callable):
            get_key = key
        else:
            raise ValueError('key is not str|callable')

        self._get_key = get_key

    def handle(self, key_value):
        def wrapper(func):
            self[key_value] = func
        return wrapper

    def callback_for(self, key_item):
        key_val = self._get_key(key_item)
        callback = self.get(key_val)

        if not callback:
            raise ValueError(f'Attempting to use key-value {key_val}, no registered handler')

        return callback
