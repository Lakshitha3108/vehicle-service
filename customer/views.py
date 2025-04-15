from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator
from django.db.models import Q
from authentication.models import Profile
from customer.models import Customer
from customer.forms import CustomerRegisterForm
from authentication.permissions import permission_roles


# Utility class to fetch customer by UUID
class GetCustomerObject:
    def get_customer(self, request, uuid):
        return Customer.objects.get(uuid=uuid, active_status=True, profile__role='Customer')


# -------------------------------
# Customer List View
# -------------------------------
@method_decorator(permission_roles(roles=['Admin']), name='dispatch')
class CustomerListView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        customers = Customer.objects.filter(active_status=True, profile__role='Customer')

        if query:
            customers = customers.filter(
                Q(profile__first_name__icontains=query) |
                Q(profile__last_name__icontains=query) |
                Q(profile__email__icontains=query) |
                Q(profile__username__icontains=query)
            )
        return render(request, "customer/customer-list.html", {'customers': customers, 'query': query})


# -------------------------------
# Customer Register View
# -------------------------------
@method_decorator(permission_roles(roles=['Admin']), name='dispatch')
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
                return redirect('customer-list')
        return render(request, "customer/customer-register.html", {'form': form})


# -------------------------------
# Customer Detail View
# -------------------------------
@method_decorator(permission_roles(roles=['Admin']), name='dispatch')
class CustomerDetailView(View):
    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        customer = GetCustomerObject().get_customer(request, uuid)
        return render(request, "customer/customer-detail.html", {'customer': customer})


# -------------------------------
# Customer Update View
# -------------------------------
@method_decorator(permission_roles(roles=['Admin']), name='dispatch')
class CustomerUpdateView(View):
    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        customer = GetCustomerObject().get_customer(request, uuid)
        form = CustomerRegisterForm(initial={
            'username': customer.profile.username,
            'email': customer.profile.email,
            'first_name': customer.profile.first_name,
            'last_name': customer.profile.last_name,
            'contact_number': customer.contact_number,
            'address': customer.address,
            'city': customer.city,
            'pincode': customer.pincode,
        })
        return render(request, "customer/customer-update.html", {'form': form, 'uuid': uuid})

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        customer = GetCustomerObject().get_customer(request, uuid)
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            profile = customer.profile
            profile.username = form.cleaned_data['username']
            profile.email = form.cleaned_data['email']
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.save()

            customer.contact_number = form.cleaned_data['contact_number']
            customer.address = form.cleaned_data['address']
            customer.city = form.cleaned_data['city']
            customer.pincode = form.cleaned_data['pincode']
            customer.save()

            return redirect('customer-list')
        return render(request, "customer/customer-update.html", {'form': form, 'uuid': uuid})


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
