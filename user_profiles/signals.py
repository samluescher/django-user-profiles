import django.dispatch

#login = django.dispatch.Signal(providing_args=["user"])

#logout = django.dispatch.Signal(providing_args=["user"])

post_signup = django.dispatch.Signal(providing_args=["user"])
"""
This signal is dispatched after a user has signed up. It is passed the
respective ``User`` instance. The ``activation`` module uses this signal to
send users a confirmation email. You can connect to this signal if you need to
execute custom code after users sign up.
"""

# for internal use only
create_user_admin_form = django.dispatch.Signal(providing_args=[])
