
from django.views import View
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class AssignServiceProviderView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if request.user.role != 'Admin':
            return redirect('login')  

        return render(request, 'service_provider/service_provider.html')

