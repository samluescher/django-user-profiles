from user_profiles import settings as app_settings
from user_profiles.utils import get_class_from_path
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views

pat = [
    url(r'^signup/$', 'user_profiles.views.signup', name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'user_profiles/login.html', 'authentication_form': get_class_from_path(app_settings.AUTHENTICATION_FORM)}, name='login'),
    url(r'^logout/$', 'user_profiles.views.logout_then_login', name='logout'),
    url(r'^pwd/reset/$', auth_views.password_reset, name='password_reset', kwargs={'template_name': 'user_profiles/password_reset_form.html', 'email_template_name': 'user_profiles/password_reset_email.html'}),
    url(r'^pwd/reset/done/$', auth_views.password_reset_done, kwargs={'template_name': 'user_profiles/password_reset_done.html'}),
    url(r'^pwd/reset/confirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'user_profiles.views.password_reset_confirm', kwargs={'template_name': 'user_profiles/password_reset_confirm.html'}),
    url(r'^you/password-change/$', 'user_profiles.views.password_change', name='password_change', kwargs={'template_name': 'user_profiles/password_change_form.html'}),
    #url(r'^profile/(.*?)/change/$', 'user_profiles.views.change', name='user_profile_change'),
    url(r'^you/change/$', 'user_profiles.views.current_user_profile_change', name='current_user_profile_change'),
    url(r'^you/$', 'user_profiles.views.current_user_detail', name='current_user_detail'),
    url(r'^profile/(.*?)/$', 'user_profiles.views.user_detail', name='user_detail'),
    # The following patterns catch URLs that have no views and redirect to the current user
    #url(r'^profile/$', 'user_profiles.views.redirect_to_current_user_detail'),
    #url(r'^$', 'user_profiles.views.redirect_to_current_user_detail'),
]

urlpatterns = patterns('', *pat)
