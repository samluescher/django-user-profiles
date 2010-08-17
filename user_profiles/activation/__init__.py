from user_profiles.activation.utils import send_activation_link_to_user
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def post_save_send_activation_link_to_new_user(sender, instance, created, *args, **kwargs):
    if created and sender == User:
        send_activation_link_to_user(instance)

post_save_send_activation_link_to_new_user
post_save.connect(post_save_send_activation_link_to_new_user)
