# service_provider/templatetags/service_provider_tags.py
from django import template
from django.urls import reverse
from customer.models import ServiceBooking  # Update to your booking app path

register = template.Library()

@register.simple_tag
def customer_booking_action(customer_profile):
    try:
        booking = ServiceBooking.objects.filter(customer=customer_profile).latest('created_at')
        if booking.status in ['Pending','Accepted','In Progress']:
            update_url = reverse('update-status', args=[booking.pk])
            return f'<a href="{update_url}" class="text-blue-600 underline">Update Status</a>'
        else:
            return 'completed'  # Don’t show anything for Completed or other statuses
    except ServiceBooking.DoesNotExist:
        return "No booking assigned"
