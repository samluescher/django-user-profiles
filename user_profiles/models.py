# coding=utf-8 
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save

User._meta.get_field('username').max_length=75

def post_save_create_profile_for_new_user(sender, **kwargs):
    from user_profiles.utils import create_profile_for_new_user
    if kwargs['created'] and sender == User:
        create_profile_for_new_user(kwargs['instance'])

post_save.connect(post_save_create_profile_for_new_user)

class UserProfileBase(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __unicode__(self):
        if hasattr(self, 'name') and self.name:
            return self.name
        elif hasattr(self, 'first_name') and hasattr(self, 'last_name') and self.first_name and self.last_name:
            return '%(first_name)s %(last_name)s' % {'first_name': self.first_name, 'last_name': self.last_name}
        else:
            if '@' in self.user.username:
                return self.user.username.split('@')[0]+u'@…'
            else:
                return self.user.username
    