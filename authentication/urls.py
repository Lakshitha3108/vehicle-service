from django.urls import path

from . import views
from .views import DashboardView,AdminDashboardView


urlpatterns = [
   
    
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    

]

