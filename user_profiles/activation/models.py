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
