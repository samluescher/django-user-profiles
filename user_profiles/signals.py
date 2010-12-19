import django.dispatch

#login = django.dispatch.Signal(providing_args=["user"])
#logout = django.dispatch.Signal(providing_args=["user"])
post_signup = django.dispatch.Signal(providing_args=["user"])
create_user_admin_form = django.dispatch.Signal(providing_args=[])
