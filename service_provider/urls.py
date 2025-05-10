from django.urls import path
from .views import AssignServiceProviderView,ServiceProviderDashboardView,BookingStatusUpdateView


urlpatterns = [
    path('assign-service/',AssignServiceProviderView.as_view(), name='assign-service'),
    path('service-provider-dashboard/',ServiceProviderDashboardView.as_view(), name='service-provider-dashboard'),
    path('booking/<int:pk>/update/', BookingStatusUpdateView.as_view(), name='update-status')

]

