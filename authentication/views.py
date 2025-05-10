from django.shortcuts import render,redirect

from django.views.generic import View

from django.contrib.auth.models import User

from .forms import LoginForm

from django.contrib.auth import authenticate,login,logout



# Create your views here.

class DashboardView(View):
      def get(self,request,*args,**kwargs):


        return render(request, "customer/dashboard.html")

    
class AdminDashboardView(View):

    def get(self,request,*args,**kwargs):


        return render(request, "authentication/admin-dashboard.html")
    
        
    


class LoginView(View):

    def get(self,request,*args,**kwargs):

        form = LoginForm()

        data = {'form':form}

        return render(request,"authentication/login.html",context=data)

    def post(self,request,*args,**kwargs):

        form = LoginForm(request.POST)

        if form.is_valid():


            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')

            user = authenticate(username=username,password=password)

            # print(user)

            # print(username,password)

            if user:

                login(request,user)

                role = user.role

                if role in ['Admin']:
                    
                 return redirect('admin-dashboard')
                
                elif role in ['Customer']:

                    return redirect('customer-dashboard')
                
                elif role in ['Service Provider']:

                    return redirect('service-provider-dashboard')
            
        error = 'user does not exist'                # here return used so we can use this method instead of using else if condition does not work it will automatically execute the next lenes
        
        data = {'form': form,'error':error}

        return render(request,'authentication/login.html',context=data)
    
class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login')  
            
        


