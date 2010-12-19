import django.dispatch

post_activation = django.dispatch.Signal(providing_args=["user"])
