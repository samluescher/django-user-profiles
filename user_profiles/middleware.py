try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

class CurrentUserMiddleware(object):
    """
    Middleware that gets user object from the
    request object and saves it in thread local storage.
    """

    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)

    @staticmethod
    def get_current_user():
        return getattr(_thread_locals, 'user', None)

    @staticmethod
    def get_current_user_groups():
        return CurrentUserMiddleware.get_current_user().groups.all()
