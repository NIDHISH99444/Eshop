from django.shortcuts import render,redirect
from django.http import HttpResponse
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
# Create your views here.


# print("password",make_password("1234"))
# print(check_password('12s34','pbkdf2_sha256$216000$85cI0RHdbvHG$/hj3lJ4EwuU0Y2x44z+xJwxAimu3XEhj0djn9IaYQoU='))

class Index(View):
    def get(self,request):
        print("inside get")
        cart=request.session.get('cart')
        if not cart : 
            request.session.cart = {}
        products =None
        categories=Category.get_all_categories()
        category_id=request.GET.get('category')
        if category_id:
            products =Product.get_all_products_by_categoryid(category_id)
        else:
            products =Product.get_all_products()
        data={}
        data['products']=products
        data['categories']=categories
        print("You are - > ",request.session.get('email'))
        return render(request,"index.html",data)

    def post(self,request):
        print("inside post")
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        
        if cart : 
            quantity=cart.get(product)
            print("qunantity",quantity)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                        print("cart is ->",cart)
                else:
                    cart[product]=quantity+1
                
            else:
                cart[product]=1
           
        else:
            cart={}
            cart[product]=1
        
        request.session['cart']=cart
        print("cart->",request.session['cart'])
        print("product",product)
        return redirect('homepage')
        




        





        