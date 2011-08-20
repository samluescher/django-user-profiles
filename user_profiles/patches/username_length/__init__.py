"""
By default, Django limits the length of the ``username`` field to 30 characters,
which is arbitrarily short, especially when you want to use email addresses as
username. This patch changes the ``max_length`` of the ``username`` field to 75
characters, same as the ``max_length`` of the ``email`` field so they can be
kept synchronized.

Install this patch by putting ``user_profiles.patches.username_length`` in your
``INSTALLED_APPS`` settings before ``django.contrib.auth``::

    INSTALLED_APPS = (
        'user_profiles.patches.username_length',
        'django.contrib.auth',
        # ...
    )

"""

from user_profiles.signals import create_user_admin_form
from django.db.models.signals import class_prepared

MAX_LENGTH = 75

def patch_user_model(sender, *args, **kwargs):
    """
    Patches the `username` field of `django.contrib.auth.models.User` to a
    `max_length` of 75 characters (EmailField default `max_length`) so it can
    store longer email addresses when using e-mail as username.
    
    As seen at
    http://stackoverflow.com/questions/2610088/can-djangos-auth-user-username-be-varchar75-how-could-that-be-done
    
    To use this, put the app on top of your INSTALLED_APPS settings. The code
    below will be executed during Django initialization/ model auto-discovery.
    """
    # You can't just do `if sender == django.contrib.auth.models.User` because
    # you would have to import the model. You have to test using __name__ and
    # __module__
    if sender.__name__ == "User" and sender.__module__ == "django.contrib.auth.models":
        import logging
        logging.warning('Patching django.contrib.auth.models.User fields `email` and `username` to `max_length=75`, make sure your database has the same limits in order to prevent truncation.')
        sender._meta.get_field("email").max_length = MAX_LENGTH
        sender._meta.get_field('username').max_length = MAX_LENGTH

class_prepared.connect(patch_user_model)

def patch_admin_forms(sender, **kwargs):
    """
    Patches the `username` field of the user creation/change forms used by `django.contrib.admin`
    to use model's `max_length` instead of hard-coded value 
    """
    if 'username' in sender.fields:
        max_length = sender.instance._meta.get_field('username').max_length
        sender.fields['username'].max_length = max_length
        sender.fields['username'].widget.attrs['maxlength'] = max_length
        sender.fields['username'].help_text =  \
            sender.fields['username'].help_text.replace('30', str(max_length))

create_user_admin_form.connect(patch_admin_forms)
