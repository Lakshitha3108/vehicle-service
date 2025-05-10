from django.urls import path
from .views import (
    CustomerListView,
    CustomerRegisterView,
    CustomerDetailView,
    HowToBookView,
    CustomerDeleteView,
    CustomerBookingView,
    CustomerDashboardView,
    BookingHistoryView
  
)
from .views import EditBookingView,DeleteBookingView



urlpatterns = [
    path('list/', CustomerListView.as_view(), name='customer-list'),
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('detail/<uuid:uuid>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('how-to-book/', HowToBookView.as_view(), name='how_to_book'),
    path('delete/<uuid:uuid>/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('book-service/', CustomerBookingView.as_view(), name='customer-booking'),
    path('customer-dashboard/', CustomerDashboardView.as_view(), name='customer-dashboard'),
    path('booking-history/', BookingHistoryView.as_view(), name='booking-history'),
    path('booking/edit/<int:pk>/', EditBookingView.as_view(), name='edit_booking'),
    path('booking/delete/<int:pk>/', DeleteBookingView.as_view(), name='delete_booking'),
    
]


    



