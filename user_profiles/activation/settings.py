from django.conf import settings

BY_EMAIL = getattr(settings, 'USER_PROFILES_ACTIVATION_BY_EMAIL', True)
