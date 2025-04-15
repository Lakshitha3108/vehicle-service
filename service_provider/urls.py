from django.urls import path
from .views import AssignServiceProviderView

urlpatterns = [
    path('assign-service/', AssignServiceProviderView.as_view(), name='assign-service'),
]