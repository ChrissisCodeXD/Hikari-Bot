from functools import wraps
import pytz
import datetime


def class_time_wrapper(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.pytz = pytz.timezone('Europe/Berlin')
        self.time = datetime.datetime.now(tz=self.pytz)
        return func(self, *args, **kwargs)

    return wrapper
