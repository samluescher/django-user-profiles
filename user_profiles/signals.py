import django.dispatch

#login = django.dispatch.Signal(providing_args=["user"])
#logout = django.dispatch.Signal(providing_args=["user"])
signup_complete = django.dispatch.Signal(providing_args=["user"])
