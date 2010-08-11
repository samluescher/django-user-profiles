from user_profiles import settings as app_settings
from user_profiles.utils import get_class_from_path
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^user/signup/$', 'user_profiles.views.signup', name='signup'),
    url(r'^user/login/$', auth_views.login, {'template_name': 'user_profiles/login.html', 'authentication_form': get_class_from_path(app_settings.AUTHENTICATION_FORM)}, name='login'),
    url(r'^user/logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^user/pwd/reset/$', auth_views.password_reset, name='password_reset', kwargs={'template_name': 'user_profiles/password_reset_form.html'}),
    url(r'^user/pwd/reset/done/$', auth_views.password_reset_done, kwargs={'template_name': 'user_profiles/password_reset_done.html'}),
    url(r'^user/pwd/reset/confirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm, kwargs={'template_name': 'user_profiles/password_reset_confirm.html'}),
    url(r'^user/pwd/reset/complete/$', auth_views.password_reset_complete, kwargs={'template_name': 'user_profiles/password_reset_complete.html'}),
    url(r'^user/pwd/change/$', auth_views.password_change, name='password_change', kwargs={'template_name': 'user_profiles/password_change_form.html'}),
    url(r'^user/pwd/change/done/$', auth_views.password_change_done, kwargs={'template_name': 'user_profiles/password_change_done.html'}),
    #url(r'^profile/(.*?)/change/$', 'user_profiles.views.change', name='user_profile_change'),
    url(r'^profile/you/change/$', 'user_profiles.views.current_user_profile_change', name='current_user_profile_change'),
    url(r'^profile/you/$', 'user_profiles.views.current_user_detail', name='current_user_detail'),
    url(r'^profile/(.*?)/$', 'user_profiles.views.user_detail', name='user_detail'),
)

