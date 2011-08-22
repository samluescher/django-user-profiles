# coding=utf-8
"""
The module ``user_profiles.models`` provides a base class for your custom user
profile model, as well as signal handlers implementing a number of requirements
when dealing with user profiles.
"""

from user_profiles import settings as app_settings
from user_profiles.utils import get_user_profile_model, sync_profile_fields
from user_profiles.managers import UserDefaultProfileManager, ByUserManager, ByCurrentUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ObjectDoesNotExist


def pre_save_email_as_username(sender, **kwargs):
    """
    This ``pre_save`` signal handler for ``User`` object is connected
    automatically if the ``USER_PROFILES_EMAIL_AS_USERNAME`` setting is enabled.
    It keeps the ``username`` and ``email`` attributes synchronized.
    """
    if sender == User:
        if not kwargs['instance'].email:
            # This applies when creating user from admin
            kwargs['instance'].email = kwargs['instance'].username
        else:
            # This applies when your profile model contains an email field and is changed
            kwargs['instance'].username = kwargs['instance'].email

            
def post_save_create_or_update_profile(sender, **kwargs):
    """
    This ``post_save`` signal handler for ``User`` and user profile objects is connected
    automatically. For new users, it creates an associated user profile
    instance. For existing users, it checks whether such an instance already
    exists, and creates one if it doesn't.
    
    Notice that this function also keeps fields of the ``User`` model
    synchronized with fields of the user profile model that have the same name.
    That is, if your user profile model contains fields named ``email`` or
    ``last_name``, their value will automatically be set to the corresponding
    attributes of the ``User`` instance when it is saved, and vice versa.
    """
    from user_profiles.utils import create_profile_for_new_user
    if sender == User and kwargs['instance'].is_authenticated():
        profile = None
        if not kwargs['created']:
            # If profile exists, copy identical field names from user to
            # profile. This assures that changing e.g. `last_name` in the admin
            # changes that field in the profile instance as well.
            try:
                profile = kwargs['instance'].get_profile()
                if len(sync_profile_fields(kwargs['instance'], profile)):
                    profile.save()
            except ObjectDoesNotExist:
                pass
        if not profile:
            # Create profile if it doesn't exist yet. This implies copying all
            # identical field names
            profile = create_profile_for_new_user(kwargs['instance'])
    if not kwargs['created'] and sender == get_user_profile_model():
        # Copy identical fields names from profile to user
        if len(sync_profile_fields(kwargs['instance'], kwargs['instance'].user)):
            kwargs['instance'].user.save()

if app_settings.EMAIL_AS_USERNAME:
    pre_save.connect(pre_save_email_as_username)
post_save.connect(post_save_create_or_update_profile)


class UserProfileBase(models.Model):
    """
    An abstract base class for your custom user profile model, defining a few
    commonly used methods, as well as the field :attr:`is_default` which enables
    you to implement a multiple-profiles-per-user feature.
    
    That field is a boolean specifying whether a specific instance is a user's
    default profile and thus will be returned by that user's ``get_profile()``
    method.

    .. note::
       If in your project every user only has one profile, you can just ignore
       the ``is_default`` field.
    
    When you subclass this class, the default ``Manager`` of your custom user
    profile model (:attr:`objects`) will only return instances whose
    ``is_default`` attribute is ``True``, that is, by default a call to
    ``MyProfileModel.objects.all()`` will only return the default profile for
    each user. See the :attr:`by_current_user` ``Manager`` for information on
    how to access all of an individual user's profiles, or :attr:`by_any_user`
    for access to any profile.

    Instead of using :attr:`by_any_user`, you can also create a proxy model of
    your user profile model, whose default ``Manager`` will give you access to
    all user profile instances. Such a proxy model could be linked to a
    ``ModelAdmin``, since site administrators would typically need access to all
    profiles instead of just one individual user's profiles.
    
    .. warning::
       If you are implementing a multiple-profiles-per-user feature in your
       project, you should prevent users from deleting their default profile by
       checking first whether ``is_default`` is ``True``. When creating
       additonal profiles for a user, you also need to make sure that the
       ``is_default`` field is ``True`` for exactly one profile object so as not
       to create any ambiguities that lead to errors. 

    """

    is_default = models.BooleanField(_('is default profile'), editable=False, default=False)
    """
    A boolean field specifying whether an instance is a user's default profile.
    This attribute is always set to ``True`` when creating an instance of your
    user profile model.
    """

    class Meta:
        abstract = True
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    # TODO: Should not set this for proxy models?
    objects = UserDefaultProfileManager()
    """
    The default ``Manager`` instance providing access to user's default profile
    instances only. See :attr:`by_current_user` and :attr:`by_any_user` for
    information on how to access user's secondary profiles.
    """

    by_current_user = ByCurrentUserManager()
    """
    A ``Manager`` instance providing access to the user profile instances
    created by the currently logged-in user only.

    If you are implementing a multiple-profiles-per-user feature, you can use
    this ``Manager`` in views that give users access to all of the user profiles
    they created, for instance::
    
        # example view displaying an individual user's profiles
        
        from user_profiles.utils import get_user_profile_model
        from django.shortcuts import render_to_response
        
        def user_profile_list(request):
            profiles = get_user_profile_model().by_current_user.all()
            return render_to_response('user_profile_list.html', {
                "profiles": profiles
            })
        
    """

    by_any_user = models.Manager()
    """
    An instance of Django's default ``Manager`` class providing access to all
    profiles created by all users.
    
    You can use this ``Manager`` in the ``queryset()`` method of your
    ``ModelAdmin`` class, since site administrators would typically need access
    to all profiles instead of just one individual user's profiles::
    
        def queryset(self, request, queryset):
            return MyUserProfileModel.by_any_user.all()
    
    """
    
    by_user = ByUserManager().by_user
    
    def __init__(self, *args, **kwargs):
        super(UserProfileBase, self).__init__(*args, **kwargs)
        # As explained in docstring of this class: ``is_default`` attribute
        # is always set to ``True`` for user profile model.
        if self.__class__ == get_user_profile_model():
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
        """
        Returns a concatenated combination of ``first_name`` and ``last_name``
        depending on whether those fields exist in your user profile model.
        """
        if hasattr(self, 'first_name') and hasattr(self, 'last_name') and self.first_name and self.last_name:
            return '%(first_name)s %(last_name)s' % {'first_name': self.first_name, 'last_name': self.last_name}
        else:
            return ''
    full_name.verbose_name = _('Name')
