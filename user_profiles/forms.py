from user_profiles import settings as app_settings
from user_profiles.utils import get_user_profile_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as ContribAuthAuthenticationForm
from django import forms


class AuthenticationForm(ContribAuthAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        if app_settings.EMAIL_AS_USERNAME:
            self.fields['username'] = forms.CharField(label=_("E-mail address"),  \
                max_length=User._meta.get_field('email').max_length)
        else:
            self.fields['username'] = forms.CharField(label=_("Username"),  \
                max_length=User._meta.get_field('username').max_length)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_profile_model()

class SignupForm(UserCreationForm):

    email = forms.EmailField(required=True, label=_('E-mail address'), help_text=_('Your e-mail address is your username. You need to provide a valid address to log in.'))
    
    def save(self, commit=True):
        from user_profiles import settings as app_settings
        user = super(SignupForm, self).save(commit=False)
        user.is_active = app_settings.USER_SET_ACTIVE_ON_SIGNUP
        if commit:
            user.save()
        return user


# TODO not working -- maybe inheritance is not the best way
class SignupWithProfileForm(SignupForm, ProfileForm):

    class Meta:
        model = get_user_profile_model()
    
    def save(self, *args, **kwargs):
        return SignupForm(self.cleaned_data).save(*args, **kwargs)

# TODO remove and replace with EMAIL_AS_USERNAME setting
class EmailAsUsernameSignupForm(SignupForm):
    email = forms.EmailField(required=True, label=_('E-mail address'), help_text=_('Your e-mail address is your username. You need to provide a valid address to log in.'))

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(EmailAsUsernameSignupForm, self).__init__(*args, **kwargs)
        del(self.fields['username'])

    def clean_email(self):
        if User.objects.filter(Q(email=self.cleaned_data['email']) | Q(username=self.cleaned_data['email'])).exists():
            raise forms.ValidationError(_('A user with this e-mail address already exists.'))
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super(EmailAsUsernameSignupForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user
