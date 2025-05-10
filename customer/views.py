from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator
from django.db.models import Q
from authentication.models import Profile
from customer.models import Customer
from customer.forms import CustomerRegisterForm
from authentication.permissions import permission_roles
from . forms import ServiceBookingForm
from . models import ServiceBooking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView



# Utility class to fetch customer by UUID
class GetCustomerObject:
    def get_customer(self, request, uuid):
        return Customer.objects.get(uuid=uuid, active_status=True, profile__role='Customer')


# Customer list view
@method_decorator(permission_roles(roles=['Admin']), name='dispatch')
class CustomerListView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        status = request.GET.get('status')
        customers = Customer.objects.filter(active_status=True, profile__role='Customer')

        if query:
            customers = customers.filter(
                Q(profile__first_name__icontains=query) |
                Q(profile__last_name__icontains=query) |
                Q(profile__email__icontains=query) |
                Q(profile__username__icontains=query)
            )
        if status in ['Pending', 'Completed']:
            customers = customers.filter(
                profile__service_bookings__status=status
            ).distinct()  

        return render(request, "customer/customer-list.html", {'customers': customers, 'query': query,'status': status,})
# @method_decorator(permission_roles(roles=['Admin']), name='dispatch')
# class CustomerListView(View):
#     model = Customer
#     template_name = 'customer-list.html'
#     context_object_name = 'customers'

#     def get(self, request, *args, **kwargs):
#         query = request.GET.get('query')
#         status_filter = request.GET.get('status')

#         # Base query
#         customers = Customer.objects.filter(active_status=True, profile__role='Customer')

#         if query:
#             customers = customers.filter(
#                 Q(profile__first_name__icontains=query) |
#                 Q(profile__last_name__icontains=query) |
#                 Q(profile__email__icontains=query) |
#                 Q(profile__username__icontains=query)
#             )

#         if status_filter:
#             customers = customers.filter(profile__service_bookings__status=status_filter).distinct()
#             print(customers.query)

#         return render(request, "customer/customer-list.html", {
#             'customers': customers,
#             'query': query,
#             'selected_status': status_filter,
#         })



# -------------------------------
# Customer Register View
# -------------------------------
# @method_decorator(permission_roles(roles=['Admin','Customer']), name='dispatch')
class CustomerRegisterView(View):
    def get(self, request, *args, **kwargs):
        form = CustomerRegisterForm()
        return render(request, "customer/customer-register.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                profile = Profile.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    role='Customer',
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )

                Customer.objects.create(
                    profile=profile,
                    contact_number=form.cleaned_data['contact_number'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    pincode=form.cleaned_data['pincode']
                )

               
                # ✅ Send welcome email after registration
                subject = 'Welcome to CarServ!'
                message = '''
                    <html>
                        <body style="font-family: Arial, sans-serif; background-color: #e9ecef; color: #495057; margin: 0; padding: 0;">
                            <table style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
                                <tr>
                                    <td style="background-color: #343a40; color: white; text-align: center; padding: 20px; border-radius: 10px 10px 0 0;">
                                        <h2 style="font-size: 24px; margin: 0;">Welcome to CarServ!</h2>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 20px; font-size: 16px; line-height: 1.6; text-align: center;">
                                        <p>Thank you for registering with CarServ. We’re excited to serve your vehicle needs!</p>
                                        <p>If you have any questions, feel free to reach out to us. We're here to help!</p>
                                        <br>
                                        <p style="font-size: 14px; color: #6c757d;">Best regards,<br>The CarServ Team</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="background-color: #f8f9fa; text-align: center; padding: 10px; border-radius: 0 0 10px 10px;">
                                        <p style="font-size: 12px; color: #6c757d;">You received this email because you registered with CarServ.</p>
                                    </td>
                                </tr>
                            </table>
                        </body>
                    </html>
                '''
                send_mail(
                    subject,
                    message,  # This is the plain-text message
                    settings.DEFAULT_FROM_EMAIL,
                    [profile.email],
                    fail_silently=False,
                    html_message=message  # The HTML content for better email design
                )
                
                return redirect('login')
        return render(request, "customer/customer-register.html", {'form': form})


# -------------------------------
# Customer Detail View
# -------------------------------
@method_decorator(permission_roles(roles=['Admin','Customer']), name='dispatch')
class CustomerDetailView(View):
    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        customer = GetCustomerObject().get_customer(request, uuid)
        bookings = ServiceBooking.objects.filter(customer=customer.profile)
        return render(request, "customer/customer-detail.html", {'customer': customer ,'bookings': bookings})


class HowToBookView(TemplateView):
    template_name = 'customer/how_to_book.html'

# -------------------------------
# Customer Delete (Soft Delete)
# -------------------------------
@method_decorator(permission_roles(roles=['Admin']), name='dispatch')
class CustomerDeleteView(View):
    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        customer = GetCustomerObject().get_customer(request, uuid)
        customer.active_status = False
        customer.save()
        return redirect("customer-list")
    
class CustomerDashboardView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(profile=request.user)
        except Customer.DoesNotExist:
            return redirect('login')  # or show error

        bookings = ServiceBooking.objects.filter(customer=request.user).order_by('-created_at')
        return render(request, 'customer/customer-dashboard.html', {'bookings': bookings})

    
@method_decorator(permission_roles(roles=['Customer']), name='dispatch')
class CustomerBookingView(View):
    def get(self, request, *args, **kwargs):
        form = ServiceBookingForm()
        return render(request, 'customer/customer-booking.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            try:
                customer = Customer.objects.get(profile=request.user)
                booking.customer = customer.profile
                booking.save()

                messages.success(request, "Service booking submitted successfully!")
                return redirect('customer-dashboard')
            except Customer.DoesNotExist:
                return redirect('login')  # or handle gracefully
        return render(request, 'customer/customer-booking.html', {'form': form})
@method_decorator(permission_roles(roles=['Customer']), name='dispatch')
class BookingHistoryView(View):
    def get(self, request,*args,**kwargs):
        bookings = ServiceBooking.objects.filter(customer=request.user).order_by('-created_at')
        return render(request, 'customer/booking-history.html', {'bookings': bookings})        
    
class EditBookingView(UpdateView):
    model = ServiceBooking  # Model we are updating
    fields = ['vehicle_model', 'service_type', 'preferred_date', 'description']  # Fields we want to allow editing
    template_name = 'customer/edit_booking.html'  # The template to render
    success_url = reverse_lazy('customer-dashboard')    

class DeleteBookingView(DeleteView):
    model = ServiceBooking
    template_name = 'customer/delete_booking.html'  # You can create this template to confirm the deletion

    # Redirect back to the book-service page after successful deletion
    success_url = reverse_lazy('customer-dashboard')   