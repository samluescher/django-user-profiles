from user_profiles.utils import get_user_profile_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_profile_model()

class SignupForm(UserCreationForm):
    
    def save(self, commit=True):
        from user_profiles import settings as app_settings
        user = super(SignupForm, self).save(commit=False)
        user.is_active = app_settings.USER_IS_ACTIVE_ON_SIGNUP
        if commit:
            user.save()
        return user

class EmailAsUsernameSignupForm(SignupForm):
    email = forms.EmailField(required=True, max_length=30, label=_('E-mail address'), help_text=_('Your e-mail address is your username. You need to provide a valid address to log in.'))

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
