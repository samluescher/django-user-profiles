Configuring django-user-profiles
********************************

The following settings can be specified in your Django project's settings
module.

USER_PROFILES_SIGNUP_FORM
    Default: ``'user_profiles.forms.SignupForm'``
    
    The form class used for user signup.


USER_PROFILES_AUTHENTICATION_FORM
    Default: ``'user_profiles.forms.SignupForm'``

    The form class used for user authentication (login).

USER_PROFILES_PROFILE_FORM
    Default: ``'user_profiles.forms.SignupForm'``

    The form class used when users edit their profile.

USER_PROFILES_URL_FIELD
    Default: ``'pk'``

    The field of the user profile model used to generate URLs to profile pages.
    You could replace this by a slug field, for instance.

USER_PROFILES_USER_SET_ACTIVE_ON_SIGNUP
    Default: ``True``
    
    Specifies whether the ``is_active`` field of a user object should be set to
    ``True`` on signup, immediately enabling the user to log in. If this is
    disabled, further activation is necessary, for instance using the activation
    module provided by django-user-profiles.


USER_PROFILES_EMAIL_AS_USERNAME
    Default: ``False``

    Specifies whether email addresses should be used as usernames. If this is
    enabled, email addresses and usernames will be kept synchronized, and users
    log in with their email address instead of specifying a username. 

