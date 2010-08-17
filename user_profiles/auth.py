from django.conf import settings
from django.contrib.auth.models import User

class EmailAsUsernameModelBackend(object):
    """
    Allows admin login with usernames containing '@', to fix a pending issue: 
    http://code.djangoproject.com/ticket/8342
    """
    def authenticate(self, username=None, password=None):
        kwargs = {'username': username}
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
