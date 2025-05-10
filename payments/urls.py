from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('razorpay/<int:booking_id>/', views.RazorpayView.as_view(), name='razorpay'),
    path('verify-payment/', views.PaymentVerify.as_view(), name='verify-payment'),
    path('payment-details/<int:booking_id>/', views.PaymentDetailView.as_view(), name='payment-details'),
    path('payment-list/', views.PaymentListView.as_view(), name='payment_list')
    # path('pay-now/<int:booking_id>/', views.PayNowView.as_view(), name='pay-now'),
]


