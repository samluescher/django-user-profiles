from user_profiles.signals import create_user_admin_form
from user_profiles import settings as app_settings
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        create_user_admin_form.send(sender=self)

class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        create_user_admin_form.send(sender=self)

class CustomUserAdmin(UserAdmin): 
    
    # TODO add config switch that allows non-superusers to create users, but not set their permissions nor superuser status
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

def patch_admin_forms(sender, **kwargs):
    """
    Disables the `email` field of the user creation/change forms used by `django.contrib.admin`,
    since `pre_save_email_as_username` sets `email` = `username`
    """
    username = sender.fields['username']
    sender.fields['username'] = forms.EmailField(label=username.label, help_text=username.help_text, max_length=username.max_length)
    if 'email' in sender.fields:
        # TODO: It actually really doesn't make sense that this field is visible at all
        sender.fields['email'].widget.attrs['disabled'] = True

if app_settings.EMAIL_AS_USERNAME:
    create_user_admin_form.connect(patch_admin_forms)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
