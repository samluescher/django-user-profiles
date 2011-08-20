from django.conf import settings

SIGNUP_FORM = getattr(settings, 'USER_PROFILES_SIGNUP_FORM', 'user_profiles.forms.SignupForm')
"""
Default: ``'user_profiles.forms.SignupForm'``

The form class used for user signup.
"""

AUTHENTICATION_FORM = getattr(settings, 'USER_PROFILES_AUTHENTICATION_FORM', 'user_profiles.forms.AuthenticationForm')
"""
Default: ``'user_profiles.forms.SignupForm'``

The form class used for user authentication (login).
"""

PROFILE_FORM = getattr(settings, 'USER_PROFILES_PROFILE_FORM', 'user_profiles.forms.ProfileForm')
"""
Default: ``'user_profiles.forms.SignupForm'``

The form class used when users edit their profile.
"""

URL_FIELD = getattr(settings, 'USER_PROFILES_URL_FIELD', 'pk')
"""
Default: ``'pk'``

The field of the user profile model used to generate URLs to profile pages.
You could replace this by a slug field, for instance.
"""

USER_SET_ACTIVE_ON_SIGNUP = getattr(settings, 'USER_PROFILES_USER_SET_ACTIVE_ON_SIGNUP', True)
"""
Default: ``True``

Specifies whether the ``is_active`` field of a user object should be set to
``True`` on signup, immediately enabling the user to log in. If this is
disabled, further activation is necessary, for instance using the activation
module provided by django-user-profiles.
"""

EMAIL_AS_USERNAME = getattr(settings, 'USER_PROFILES_EMAIL_AS_USERNAME', False)
"""
Default: ``False``

Specifies whether email addresses should be used as usernames. If this is
enabled, email addresses and usernames will be kept synchronized, and users
log in with their email address instead of specifying a username. 
"""
