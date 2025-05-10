from django import forms
from django.contrib.auth import get_user_model
from customer.models import Customer
from .models import ServiceBooking
from common.choices import ServiceTypeChoices

Profile = get_user_model()

class CustomerRegisterForm(forms.ModelForm):
    # Profile fields
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Enter username',
            'required': 'required'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Enter email',
            'required': 'required'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Enter password',
            'required': 'required'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Confirm password',
            'required': 'required'
        })
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Enter first name',
            'required': 'required'
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
            'placeholder': 'Enter last name',
            'required': 'required'
        })
    )

    class Meta:
        model = Customer
        fields = ['contact_number', 'address', 'city', 'pincode']
        widgets = {
            'contact_number': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Enter contact number',
                'required': 'required'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Enter address',
                'rows': 3,
                'required': 'required'
            }),
            'city': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Enter city',
                'required': 'required'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                'placeholder': 'Enter pincode',
                'required': 'required'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        pincode = cleaned_data.get("pincode")
        vehicle_number = cleaned_data.get("vehicle_number")
        
        if Profile.objects.filter(email=email).exists():
            self.add_error('email', 'Email is already registered. Please choose another.')

        if pincode and len(pincode) != 6:
            self.add_error('pincode', 'Pincode must be exactly 6 digits.')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
       
    

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
          super(CustomerRegisterForm, self).__init__(*args, **kwargs)

    # Apply styling to ModelForm fields (from Customer model)
          for field_name in self.fields:
            field = self.fields[field_name]
            if not field.widget.attrs.get('class'):
              field.widget.attrs['class'] = 'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input'
        
        # Add placeholder dynamically if not present
            if not field.widget.attrs.get('placeholder'):
              field.widget.attrs['placeholder'] = f'Enter {field_name.replace("_", " ")}'

        # Mark all fields as required (except confirm_password which is manually validated)
            if field_name != 'confirm_password':
              field.widget.attrs['required'] = 'required'

class ServiceBookingForm(forms.ModelForm):
    
    class Meta:
        model = ServiceBooking
        fields = ['vehicle_model', 'service_type', 'preferred_date', 'description','vehicle_number']
        widgets = {
            'vehicle_model': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'Enter vehicle model'
            }),
             'vehicle_number': forms.TextInput(attrs={  
                'class': 'form-input', 'placeholder': 'Enter vehicle number'
            }),

            'service_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea', 'rows': 3, 'placeholder': 'Additional notes (optional)'
            }),
        }          

    
    def clean(self):
        cleaned_data = super().clean()
        vehicle_number = cleaned_data.get("vehicle_number")
        
        # Validation for vehicle number
        if vehicle_number:
            import re
            pattern = r'^KL\d{2}[A-Z]{1,2}\d{4}$'
            formatted_number = vehicle_number.replace(" ", "").upper()
            
            if not re.match(pattern, formatted_number):
                self.add_error('vehicle_number', 'Enter a valid vehicle number.')
        
        return cleaned_data

   