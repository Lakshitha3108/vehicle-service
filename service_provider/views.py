
from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from service_provider.models import ServiceProvider
from customer.models import Customer,ServiceBooking
from common.choices import BookingStatusChoices
from authentication.permissions import permission_roles
from django.contrib import messages
from payments.models import Payment,PaymentStatusChoices
from django.core.mail import send_mail
from django.conf import settings




class AssignServiceProviderView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if request.user.role != 'Admin':
            return redirect('login')  

        customers = Customer.objects.all()
        service_providers = ServiceProvider.objects.filter(is_available=True)
        return render(request, 'service_provider/assign_service_provider.html', {
            'customers': customers,
            'service_providers': service_providers
        })

    def post(self, request):
        if request.user.role != 'Admin':
            return redirect('login')

        customer_uuid = request.POST.get('customer')
        provider_uuid = request.POST.get('service_provider')

        customer = get_object_or_404(Customer, uuid=customer_uuid)
        provider = get_object_or_404(ServiceProvider, uuid=provider_uuid)
          

        booking = ServiceBooking.objects.filter(customer=customer.profile).order_by('-created_at').first()

        if not booking:
            messages.error(request, "No booking found for this customer.")
        elif provider.expertise != booking.service_type:
            messages.error(
                request,
                f"Wrong assignment: Booking requires '{booking.service_type}' but provider is '{provider.expertise}'."
            )
        else:
            customer.assigned_provider = provider
            customer.save()
            booking.service_provider = provider
            booking.save()
            messages.success(request, "Service provider assigned successfully.")
            return redirect('customer-list')

        # Re-render form with messages
        customers = Customer.objects.all()
        service_providers = ServiceProvider.objects.filter(is_available=True)
        return render(request, 'service_provider/assign_service_provider.html', {
            'customers': customers,
            'service_providers': service_providers
        })

        # customer.assigned_provider = provider
        # customer.save()

        # return redirect('customer-list')  # Adjust as needed
    
# service_provider/views.py

class ServiceProviderDashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.role != 'Service Provider':
            return redirect('login')

        provider = get_object_or_404(ServiceProvider, user=request.user)
        assigned_customers = Customer.objects.filter(assigned_provider=provider)
        bookings = ServiceBooking.objects.filter(service_provider=provider)
        
        return render(request, 'service_provider/service-provider-dashboard.html', {
            'provider': provider,
            'assigned_customers': assigned_customers,
            'bookings' : bookings,
            
        })


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_roles(roles=['Service Provider']), name='dispatch')
class BookingStatusUpdateView(View):
    def get(self, request, pk):
        booking = get_object_or_404(ServiceBooking, id=pk)
        return render(request, 'service_provider/update-status.html', {
            'booking': booking,
            'status_choices': BookingStatusChoices.choices,
        })

    


    def post(self, request, pk):
        booking = get_object_or_404(ServiceBooking, id=pk)
       
        new_status = request.POST.get('status')

        print(f"Received status: {new_status}")

        if new_status in dict(BookingStatusChoices.choices).keys():
           booking.status = new_status
           booking.save()

        # If status is "Completed", create a payment and send email
           if new_status == BookingStatusChoices.COMPLETED:
                customer = Customer.objects.get(profile=booking.customer)
                Payment.objects.create(
                service=booking,
                amount=200,
                customer=customer,
                status=PaymentStatusChoices.SUCCESS
            )
                subject = "Your Vehicle Service is Complete"
                message = f"""
Hi {booking.customer.first_name},

Your service for the vehicle model {booking.vehicle_model} has been marked as Completed.

Please log in to your dashboard and click the "Pay Now" button to complete the payment.
Once paid, you can collect your vehicle from the service center.

Thank you for choosing our service!

Best regards,  
Vehicle Service Management Team
"""
                recipient = [booking.customer.email]
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)
                messages.success(request, "Booking status updated successfully!")
        else:
               messages.error(request, "Invalid status selected.")

        return redirect('service-provider-dashboard')  # update this as needed