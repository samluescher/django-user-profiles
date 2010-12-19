from django.contrib.auth.models import User
from user_profiles.signals import post_signup
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import uuid

class ActivationCode(models.Model):
    key = models.CharField(max_length=32, editable=False)
    user = models.ForeignKey(User, editable=False)
    activated = models.BooleanField(editable=False, default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex
        super(ActivationCode, self).save(*args, **kwargs)

def post_signup_send_activation_link_to_new_user(sender, **kwargs):
    from user_profiles.activation.utils import send_activation_link_to_user
    send_activation_link_to_user(kwargs['user'], created=True)

post_signup.connect(post_signup_send_activation_link_to_new_user)
