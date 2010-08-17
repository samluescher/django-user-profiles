import django.dispatch

activation_complete = django.dispatch.Signal(providing_args=["user"])
