from django.contrib.auth.models import User
from django.db.models.signals import post_save
from user_profiles.utils import get_user_profile_model

def create_profile_for_user(sender, instance, created, *args, **kwargs):
    if created and sender == User:
        model = get_user_profile_model()
        model(user=instance).save()
        
post_save.connect(create_profile_for_user)
