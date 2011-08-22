"""
You can subclass any of the following form classes if you need to customize your
signup, login or profile editing processes.
"""

from user_profiles import settings as app_settings
from user_profiles.utils import get_user_profile_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as ContribAuthAuthenticationForm
from django import forms


class AuthenticationForm(ContribAuthAuthenticationForm):
    """
    The basic login form, based on Django's default authentication form.
    """
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        if app_settings.EMAIL_AS_USERNAME:
            self.fields['username'] = forms.CharField(label=_("E-mail address"),  \
                max_length=User._meta.get_field('email').max_length)
        else:
            self.fields['username'] = forms.CharField(label=_("Username"),  \
                max_length=User._meta.get_field('username').max_length)


class ProfileForm(forms.ModelForm):
    """
    The basic user profile form. This is simply a ``ModelForm`` for the user
    profile model.
    """
    class Meta:
        model = get_user_profile_model()

class SignupForm(UserCreationForm):
    """
    The basic signup form, based on Django's ``UserCreationForm`` form.

    Signup forms are different from user profile forms in that you might want to
    keep it as simple as possible, i.e. require just the most basic information
    during signup, in order not to overwhelm the user. 
    
    This form's ``save()`` method handles a few extra tasks, such as creating
    initially inactive user accounts if you configured your project
    appropriately. See :ref:`activation`.
    """

    email = forms.EmailField(required=True, label=_('E-mail address'))

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        if app_settings.EMAIL_AS_USERNAME:
            del self.fields['username']
            self.fields.insert(0, 'email', self.fields.pop('email'))
            self.fields['email'].help_text = _('Your e-mail address is your username. You need to provide a valid address to log in.')
        else:
            self.fields['email'].help_text = _('You need to provide a valid address.')
            
    def clean_email(self):
        if User.objects.filter(Q(email=self.cleaned_data['email']) | Q(username=self.cleaned_data['email'])).exists():
            raise forms.ValidationError(_('A user with this e-mail address already exists.'))
        return self.cleaned_data['email']
    
    def save(self, commit=True):
        from user_profiles import settings as app_settings
        user = super(SignupForm, self).save(commit=False)
        user.is_active = app_settings.USER_SET_ACTIVE_ON_SIGNUP
        if commit:
            user.save()
        return user


# TODO not working -- maybe inheritance is not the way to do it
class SignupWithProfileForm(SignupForm, ProfileForm):
    """
    NOT IMPLEMENTED. Signup form requiring users to fill in their full profile
    during signup.
    """

    class Meta:
        model = get_user_profile_model()
    
    def save(self, *args, **kwargs):
        return SignupForm(self.cleaned_data).save(*args, **kwargs)

