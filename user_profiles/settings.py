from django.conf import settings
from user_profiles.forms import SignupForm, ProfileForm

SIGNUP_FORM = getattr(settings, 'USER_PROFILES_SIGNUP_FORM', 'user_profiles.forms.SignupForm')
PROFILE_FORM = getattr(settings, 'USER_PROFILES_PROFILE_FORM', 'user_profiles.forms.ProfileForm')
AUTHENTICATION_FORM = getattr(settings, 'USER_PROFILES_AUTHENTICATION_FORM', 'django.contrib.auth.forms.AuthenticationForm')

URL_FIELD = getattr(settings, 'USER_PROFILES_URL_FIELD', 'pk')
