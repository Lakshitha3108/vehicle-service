from django.shortcuts import render
from django.views import View

# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/home.html')

class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/contact.html')

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/about.html')
