# service_provider/forms.py
from django import forms
from customer.models import Customer
from .models import ServiceProvider

class AssignServiceProviderForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), label="Select Customer")
    service_provider = forms.ModelChoiceField(queryset=ServiceProvider.objects.filter(is_available=True), label="Select Service Provider")
