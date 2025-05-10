from django.db import models

class ServiceTypeChoices(models.TextChoices):
    OIL_CHANGE = 'OIL_CHANGE', 'Oil Change'
    ENGINE_REPAIR = 'ENGINE_REPAIR', 'Engine Repair'
    TIRE_REPLACEMENT = 'TIRE_REPLACEMENT', 'Tire Replacement'
    BRAKE_SERVICE = 'BRAKE_SERVICE', 'Brake Service'
    GENERAL_CHECKUP = 'GENERAL_CHECKUP', 'General Checkup'


class BookingStatusChoices(models.TextChoices):
    PENDING = "Pending", "Pending"
    ACCEPTED = "Accepted", "Accepted"
    IN_PROGRESS = "In Progress", "In Progress"
    COMPLETED = "Completed", "Completed"
    REJECTED = "Rejected", "Rejected"

