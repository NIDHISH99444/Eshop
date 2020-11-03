from django.shortcuts import render,redirect
from django.http import HttpResponse
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
# Create your views here.


class Signup(View):
    def get(self,request):
        return render(request,"signup.html")

    def post(self,request):
         
        postData=request.POST
        first_name=postData.get("firstname")
        last_name=postData.get("lastname")
        phone=postData.get("phone")
        email=postData.get("email")
        password=postData.get("password")
        #validation
        value={
            'first_name':first_name,
            'last_name' : last_name,
            'phone' : phone, 
            'email' : email,
        
        }
        error_message=None
        customer=Customer(first_name=first_name,last_name=last_name,
            phone=phone, email=email, password=password)
        error_message=self.validateCustomer(customer)

        #save
        if not error_message:
            print(first_name,last_name,phone,email,password)
            print(customer.password)
            customer.password=make_password(customer.password)
            customer.register()
            return redirect("homepage")
        else:
            data ={
                'error':error_message,
                'values': value
                }
            return render(request,"signup.html",data)


    def validateCustomer(self,customer):
        error_message=None
        if (not customer.first_name):
            error_message="First name required"
        elif len(customer.first_name) < 4 : 
                error_message= "First name must be more than 4 letters"
        if not customer.last_name:
            error_message="Last name required"
        elif len(customer.last_name) < 4 : 
                error_message= "Last name must be more than 4 letters"
        elif not customer.phone : 
            error_message  ="Phone no required"  
        elif len(customer.phone)<10 :
            error_message= "Not a valid phone number"
        elif len(customer.password)< 6 :
            error_message="Pass must be 6 char long"
        elif len(customer.email)< 5 :
            error_message="Email must be 5 char long "
        elif customer.isExists():
            error_message = "Email Address already registered"
        return error_message