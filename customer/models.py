from django.db import models
from django.conf import settings
import uuid
class ServiceTypeChoices(models.TextChoices):
    OIL_CHANGE = 'OIL_CHANGE', 'Oil Change'
    ENGINE_REPAIR = 'ENGINE_REPAIR', 'Engine Repair'
    TIRE_REPLACEMENT = 'TIRE_REPLACEMENT', 'Tire Replacement'
    BRAKE_SERVICE = 'BRAKE_SERVICE', 'Brake Service'
    GENERAL_CHECKUP = 'GENERAL_CHECKUP', 'General Checkup'

class Customer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name}"    

class ServiceBooking(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=100)

    service_type = models.CharField(
        max_length=50,
        choices=ServiceTypeChoices.choices,
        default=ServiceTypeChoices.GENERAL_CHECKUP,
    )

    preferred_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_model} - {self.get_service_type_display()}"
