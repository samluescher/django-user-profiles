from user_profiles.utils import get_user_profile_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_profile_model()

class SignupForm(forms.Form):
    username = forms.CharField(label=_('username'), required=True, max_length=30)
    password = forms.CharField(label=_('Password'), required=True, max_length=128, widget=forms.widgets.PasswordInput)
    password_confirm = forms.CharField(label=_('Password confirmation'), help_text=_('Please enter your password again to verify you typed it in correctly.'), required=True, widget=forms.widgets.PasswordInput)

    class Meta:
        model = User
    
    def clean_username(self):
        existing_user = User.objects.filter(username=self.cleaned_data['username'])
        if existing_user.exists():
            raise forms.ValidationError(_('This username is already taken.'))
        return self.cleaned_data['username']

    def clean_password_confirm(self):
        if 'password' in self.cleaned_data and self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError(_('Password confirmation does not match password.'))
        return self.cleaned_data['password_confirm']
        
    def save(self, commit=True):
        new_user = User(username=self.cleaned_data['username'], 
            email=self.cleaned_data.get('email', ''))
        new_user.set_password(self.cleaned_data.get('password', ''))
        if commit:
            new_user.save()
        return new_user
