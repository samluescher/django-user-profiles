from user_profiles.middleware import CurrentUserMiddleware
from django.db import models


class CreatedByCurrentUserManager(models.Manager):
    # TODO make field configurable
    def get_query_set(self):
        user = CurrentUserMiddleware.get_current_user()
        if not user or not user.is_authenticated():
            user = None
        return super(CreatedByCurrentUserManager, self).get_query_set().filter(created_by=user)


class UserDefaultProfileManager(models.Manager):
    def get_query_set(self):
        return super(UserDefaultProfileManager, self).get_query_set().filter(is_default=True)

