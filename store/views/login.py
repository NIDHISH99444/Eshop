from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.contrib.auth.hashers import make_password,check_password
from django.views import View


class Login(View):
    return_url= None
    def get(self,request):
        print("GET")
        Login.return_url = request.GET.get('return_url')
        print(Login.return_url)
        return render(request,'login.html')

    def post(self,request):
        print("POST")
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        customer=Customer.getCustomer_by_email(email)
        error_message=None
        if customer:
            flag=check_password(password,customer.password)
            if flag:
                print(customer.id,customer.email)
                request.session['customer'] = customer.id 
                if Login.return_url:
                    print("Login return url",Login.return_url)
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url=None
                    print("over here")
                    print("Login return url",Login.return_url)
                    return redirect("homepage") 
            else:
                error_message="Email or password is invalid "    
        else:
            error_message="Email or password is invalid "

        return render(request,'login.html',{'error': error_message})



def logout(request):
    request.session.clear()
    return redirect("login")