from django.contrib.auth.models import User
from django.db.models.signals import post_save

def post_save_create_profile_for_new_user(sender, **kwargs):
    from user_profiles.utils import create_profile_for_new_user
    if kwargs['created'] and sender == User:
        create_profile_for_new_user(kwargs['instance'])

post_save.connect(post_save_create_profile_for_new_user)