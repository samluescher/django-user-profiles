"""
django-user-profiles includes a few model managers for commonly used tasks, for
instance to retrieve all objects created by a specific user.
"""

from user_profiles.middleware import CurrentUserMiddleware
from django.db import models


class ByUserManager(models.Manager):
    """
    A manager for accessing all objects created by a specific user.
    
    You can pass the name of the field that is storing the user when creating an
    instance of this class. If omitted, the default field is ``created_by``.
    
    Example usage::
    
        class MyModel(models.Model):
            created_by = models.ForeignKey(User)
            objects = ByUserManager()
            
    With this model, ``MyModel.objects.all()`` will return all objects, while
    ``MyModel.objects.by_user(some_user)`` will return all objects created by
    the specified user, which is a handy shortcut instead of using the more
    verbose ``MyModel.objects.filter(user=some_user)``.
    """
    
    user_field = 'created_by'

    def __init__(self, user_field=None):
        super(ByUserManager, self).__init__()
        if user_field:
            self.user_field = user_field

    def by_user(self, user):
        return super(ByUserManager, self).get_query_set().filter(**{
            self.user_field: user})


class ByCurrentUserManager(ByUserManager):
    """
    A manager for accessing all objects created by the current user, based on
    ``CurrentUserMiddleware`` (see :ref:`middleware`).
    
    You can pass the name of the field that is storing the user when creating an
    instance of this class. If omitted, the default field is ``created_by``.
    
    Example usage::
    
        class MyModel(models.Model):
            created_by = models.ForeignKey(User)
            by_current_user = ByCurrentUserManager()
            
    With this model, ``MyModel.objects.all()`` will return all objects, while
    ``MyModel.by_current_user.all()`` will return all objects created by the
    current user.
    """

    def get_query_set(self):
        user = CurrentUserMiddleware.get_current_user()
        if not user or not user.is_authenticated():
            user = None
        return self.by_user(user)


class UserDefaultProfileManager(ByUserManager):
    def get_query_set(self):
        return super(UserDefaultProfileManager, self).get_query_set().filter(is_default=True)

