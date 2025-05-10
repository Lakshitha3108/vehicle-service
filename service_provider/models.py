from django.db import models
from authentication.models import Profile
import uuid
from common.choices import ServiceTypeChoices

class ServiceProvider(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100,choices=ServiceTypeChoices.choices)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

