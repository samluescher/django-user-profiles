from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^activation/send/$', 'user_profiles.activation.views.current_user_send', name='user_profiles_activation_current_user_send'),
    url(r'^activation/([a-z0-9]+)/$', 'user_profiles.activation.views.activate', name='user_profiles_activation_activate'),
    url(r'^activation/$', 'user_profiles.activation.views.activate', name='user_profiles_activation_form'),
)

