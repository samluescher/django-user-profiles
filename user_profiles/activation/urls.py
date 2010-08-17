from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^activation/resend/$', 'user_profiles.activation.views.current_user_resend', name='user_profiles_activation_current_user_resend'),
    url(r'^activation/([a-z0-9]+)/$', 'user_profiles.activation.views.activate', name='user_profiles_activation_activate'),
    url(r'^activation/$', 'user_profiles.activation.views.activate', name='user_profiles_activation_form'),
)

