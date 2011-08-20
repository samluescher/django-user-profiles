try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

class CurrentUserMiddleware(object):
    """
    Standard middleware that gets user object from the request object and saves
    it in thread local storage so that it can be retrieved from contexts where
    no ``request`` instance is available.

    Whether the use of thread locals is good or bad is subject to debate due to
    possible `security issues, or opaqueness of the resulting code for that
    matter <http://stackoverflow.com/questions/3227180>`_, as opposed to
    `explicitly passing the user object to a function
    <http://stackoverflow.com/questions/2087531>`_. However, there are some
    contexts when a ``request`` and/or ``user`` instance are simply not
    available, such as some ``ModelAdmin`` methods, and thus the careful use of
    thread locals is justified.
    
    .. note::
       Installing :class:`CurrentUserMiddleware` is currently a requirement when
       using django-user-profiles.
    """

    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)

    @staticmethod
    def get_current_user():
        """
        Returns a ``User`` instance representing the user associated with the
        current request.
        """
        return getattr(_thread_locals, 'user', None)

    @staticmethod
    def get_current_user_groups():
        """
        Returns a ``QuerySet`` containing all groups the the user associated
        with the current request belongs to.
        """
        return CurrentUserMiddleware.get_current_user().groups.all()
