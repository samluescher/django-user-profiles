from django.conf import settings

SIGNUP_FORM = getattr(settings, 'USER_PROFILES_SIGNUP_FORM', 'user_profiles.forms.SignupForm')
PROFILE_FORM = getattr(settings, 'USER_PROFILES_PROFILE_FORM', 'user_profiles.forms.ProfileForm')
AUTHENTICATION_FORM = getattr(settings, 'USER_PROFILES_AUTHENTICATION_FORM', 'user_profiles.forms.AuthenticationForm')
URL_FIELD = getattr(settings, 'USER_PROFILES_URL_FIELD', 'pk')
USER_SET_ACTIVE_ON_SIGNUP = getattr(settings, 'USER_PROFILES_USER_SET_ACTIVE_ON_SIGNUP', True)
EMAIL_AS_USERNAME = getattr(settings, 'USER_PROFILES_EMAIL_AS_USERNAME', False)