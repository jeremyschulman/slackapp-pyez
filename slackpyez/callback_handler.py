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
            raise ValueError('Attempting to use key-value {}, no registered handler'.format(
                key_val))

        return callback

    def __call__(self, key_item, **kwargs):
        key_val = self._get_key(key_item)
        callback = self.get(key_val)

        if not callback:
            raise ValueError('Attempting to use key-value {}, no registered handler'.format(
                key_val))

        return callback(**kwargs)
