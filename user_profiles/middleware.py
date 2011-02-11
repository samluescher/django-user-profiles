import datetime

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

class CurrentUserMiddleware(object):
    """Middleware that gets user object from the
    request object and saves it in thread local storage."""

    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)

    @staticmethod
    def get_current_user():
        return getattr(_thread_locals, 'user', None)

    @staticmethod
    def get_current_user_groups():
        return CurrentUserMiddleware.get_current_user().groups.all()

class PerRequestCacheMiddleware(object):
    """Middleware 
    request object and saves it in thread local storage."""

    def process_request(self, request):
        _thread_locals.now = datetime.datetime.now()
        _thread_locals.cache = {}

    @staticmethod
    def get(key, default=None):
        return _thread_locals.cache.get(key, default)

    @staticmethod
    def set(key, value):
        _thread_locals.cache[key] = value

    @staticmethod
    def now():
        return _thread_locals.now
