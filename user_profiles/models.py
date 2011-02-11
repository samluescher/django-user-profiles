# coding=utf-8 
from user_profiles import settings as app_settings
from user_profiles.utils import get_user_profile_model, sync_profile_fields
from user_profiles.managers import UserDefaultProfileManager, CreatedByCurrentUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ObjectDoesNotExist

def pre_save_email_as_username(sender, **kwargs):
    if sender == User:
        if not kwargs['instance'].email:
            # This applies when creating user from admin
            kwargs['instance'].email = kwargs['instance'].username
        else:
            # This applies when your profile model contains an email field and is changed
            kwargs['instance'].username = kwargs['instance'].email

            
def post_save_create_or_update_profile(sender, **kwargs):
    from user_profiles.utils import create_profile_for_new_user
    if sender == User and kwargs['instance'].is_authenticated():
        profile = None
        if not kwargs['created']:
            # If profile exists, copy identical field names from user to profile. This assures that
            # changing e.g. `last_name` in the admin changes that field in the profile instance
            # as well.
            try:
                profile = kwargs['instance'].get_profile()
                if len(sync_profile_fields(kwargs['instance'], profile)):
                    profile.save()
            except ObjectDoesNotExist:
                pass
        if not profile:
            # Create profile if it doesn't exist yet. This implies copying all identical field names
            profile = create_profile_for_new_user(kwargs['instance'])
    if not kwargs['created'] and sender == get_user_profile_model():
        # Copy identical fields names from profile to user
        if len(sync_profile_fields(kwargs['instance'], kwargs['instance'].user)):
            kwargs['instance'].user.save()

if app_settings.EMAIL_AS_USERNAME:
    pre_save.connect(pre_save_email_as_username)
post_save.connect(post_save_create_or_update_profile)


class UserProfileBase(models.Model):

    is_default = models.BooleanField(_('is default profile'), editable=False, default=False)

    class Meta:
        abstract = True
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    by_current_user = CreatedByCurrentUserManager()

    def __init__(self, *args, **kwargs):
        super(UserProfileBase, self).__init__(*args, **kwargs)
        if self.__class__ == get_user_profile_model():
            self.objects = UserDefaultProfileManager()
            self.is_default = True

    def __unicode__(self):
        if hasattr(self, 'name') and self.name:
            return self.name
        else:
            full_name = self.full_name()
            if full_name:
                return full_name
            else:
                if '@' in self.user.username:
                    return self.user.username.split('@')[0]+u'@…'
                else:
                    return self.user.username

    def full_name(self):
        if hasattr(self, 'first_name') and hasattr(self, 'last_name') and self.first_name and self.last_name:
            return '%(first_name)s %(last_name)s' % {'first_name': self.first_name, 'last_name': self.last_name}
        else:
            return ''
    full_name.verbose_name = _('Name')
