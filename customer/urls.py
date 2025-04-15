from django.urls import path
from .views import (
    CustomerListView,
    CustomerRegisterView,
    CustomerDetailView,
    CustomerUpdateView,
    CustomerDeleteView,
)

urlpatterns = [
    path('list/', CustomerListView.as_view(), name='customer-list'),
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('detail/<uuid:uuid>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('update/<uuid:uuid>/', CustomerUpdateView.as_view(), name='customer-update'),
    path('delete/<uuid:uuid>/', CustomerDeleteView.as_view(), name='customer-delete'),
]
