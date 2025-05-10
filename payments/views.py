from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decouple import config
import razorpay
import datetime
from django.utils import timezone

from .models import Payment, Transactions
from customer.models import ServiceBooking, Customer
from django.contrib.auth.decorators import login_required

class RazorpayView(View):
    def get(self, request, booking_id, *args, **kwargs):
        # Ensure customer is logged in
        customer = Customer.objects.get(profile=request.user)
        
        # Get the booking details (only allow customer to pay for their own booking)
        booking = get_object_or_404(ServiceBooking, id=booking_id, customer=request.user)

        # Check if the service is marked as "Complete"
        if booking.status != 'Completed':
            return render(request, 'payments/error.html', {'message': 'Service not completed yet.'})

        # Create or retrieve payment entry
        payment, created = Payment.objects.get_or_create(service=booking, customer=customer, defaults={
            'amount': 999.00  # Replace with actual logic to calculate amount
        })

        # Razorpay client setup
        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))
        receipt_id = f"receipt_{booking.id}"

        # Data to create the order
        data = {
            "amount": int(payment.amount * 100),  # Amount in paise
            "currency": "INR",
            "receipt": receipt_id
        }
        rzp_order = client.order.create(data=data)
        order_id = rzp_order['id']

        # Store transaction
        Transactions.objects.create(payment=payment, rzp_order_id=order_id, amount=payment.amount)

        return render(request, 'payments/razorpay-page.html', {
            'order_id': order_id,
            'amount': data['amount'],
            'RZP_CLIENT_ID': config('RZP_CLIENT_ID'),
            'booking_id': booking_id,
        })

@method_decorator(csrf_exempt, name='dispatch')
# class PaymentVerify(View):
#     def post(self, request, *args, **kwargs):
#         data = request.POST

#         rzp_order_id = data.get('razorpay_order_id')
#         rzp_payment_id = data.get('razorpay_payment_id')
#         rzp_signature = data.get('razorpay_signature')

#         # Retrieve the transaction based on order ID
#         transaction = get_object_or_404(Transactions, rzp_order_id=rzp_order_id)
#         transaction.rzp_payment_id = rzp_payment_id
#         transaction.rzp_signature = rzp_signature

#         client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

#         try:
#             # Verify payment signature
#             client.utility.verify_payment_signature({
#                 'razorpay_order_id': rzp_order_id,
#                 'razorpay_payment_id': rzp_payment_id,
#                 'razorpay_signature': rzp_signature
#             })

#             # Payment verified successfully, update transaction and payment status
#             transaction.status = 'Success'
#             transaction.transaction_at = datetime.datetime.now()
#             transaction.save()

#             payment = transaction.payment
#             payment.status = 'Success'
#             payment.paid_at = datetime.datetime.now()
#             payment.save()

#             return redirect('payments:payment-details', booking_id=payment.service.id)

#         except razorpay.errors.SignatureVerificationError:
#             # Payment verification failed, update status to Failed
#             transaction.status = 'Failed'
#             transaction.transaction_at = datetime.datetime.now()
#             transaction.save()

#             return redirect('payments:payment-details', booking_id=payment.service.id)
class PaymentVerify(View):
    def post(self, request, *args, **kwargs):
        data = request.POST

        rzp_order_id = data.get('razorpay_order_id')
        rzp_payment_id = data.get('razorpay_payment_id')
        rzp_signature = data.get('razorpay_signature')

        # Retrieve the transaction based on order ID
        transaction = get_object_or_404(Transactions, rzp_order_id=rzp_order_id)
        transaction.rzp_payment_id = rzp_payment_id
        transaction.rzp_signature = rzp_signature

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': rzp_order_id,
                'razorpay_payment_id': rzp_payment_id,
                'razorpay_signature': rzp_signature
            })

            # Payment verified successfully, update transaction and payment status
            transaction.status = 'Success'
            transaction.transaction_at = timezone.now()  # Timezone-aware datetime
            transaction.save()

            payment = transaction.payment
            payment.status = 'Success'
            payment.paid_at = timezone.now()  # Timezone-aware datetime
            payment.save()

            return redirect('payments:payment-details', booking_id=payment.service.id)

        except razorpay.errors.SignatureVerificationError:
            # Payment verification failed, update status to Failed
            transaction.status = 'Failed'
            transaction.transaction_at = timezone.now()  # Timezone-aware datetime
            transaction.save()

            return redirect('payments:payment-details', booking_id=payment.service.id)

class PaymentDetailView(View):
    def get(self, request, booking_id, *args, **kwargs):
        # Retrieve booking and validate user
        booking = get_object_or_404(ServiceBooking, id=booking_id)

        if request.user == booking.customer or request.user.is_superuser:
            payment = get_object_or_404(Payment, service=booking)
            transaction = Transactions.objects.filter(payment=payment).first()
           

            return render(request, 'payments/payment-details.html', {
                'payment': payment,
                'transaction': transaction,
                'booking':booking
            })

        return render(request, 'payments/error.html', {'message': 'Unauthorized access to payment details.'})
 
class PaymentListView(View):
    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            payments = Payment.objects.all()
        else:
            customer = Customer.objects.get(profile=request.user)
            payments = Payment.objects.filter(service__customer=customer)
        return render(request, 'payments/payment_list.html', {'payments': payments})

    
 
