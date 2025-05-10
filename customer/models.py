from django.db import models
from django.conf import settings
import uuid
from service_provider.models import ServiceProvider
from common.choices import ServiceTypeChoices,BookingStatusChoices

class Customer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    active_status = models.BooleanField(default=True)
    assigned_provider = models.ForeignKey(ServiceProvider,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_customers')


    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name}"    

class ServiceBooking(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='service_bookings')
    
    service_provider = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.SET_NULL, null=True, blank=True)

    vehicle_number = models.CharField(max_length=20, blank=True, null=True)

    vehicle_model = models.CharField(max_length=100)

    service_type = models.CharField(
        max_length=50,
        choices=ServiceTypeChoices.choices,
        default=ServiceTypeChoices.GENERAL_CHECKUP,
    )

    preferred_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=BookingStatusChoices.choices,
        default=BookingStatusChoices.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_model} - {self.get_service_type_display()}"
