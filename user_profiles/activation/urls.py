from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^activation/send/$', 'user_profiles.activation.views.send_activation_code_to_user', name='user_profiles_send_activation_code_to_user'),
    url(r'^activation/([a-z0-9]+)/$', 'user_profiles.activation.views.activate', name='user_profiles_activate'),
    url(r'^activation/$', 'user_profiles.activation.views.activate', name='user_profiles_activation_form'),
)

