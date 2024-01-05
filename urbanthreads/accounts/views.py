from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
from .models import *
from store.models import Clothing
import uuid
import json
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404) 
from django.contrib.auth import (
    authenticate,
    login as auth_login
)
from cart.utils import user_cookies
from .utils import process_guest_cookies

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            auth_login(request, user)
            response = redirect('accounts:user_profile')
            cookie_cart = request.COOKIES.get('cart')
            if cookie_cart:
                process_guest_cookies(request,cookie_cart,user)
                response.set_cookie('cart',user_cookies(request))  
                return response     
            else:
                response.set_cookie('cart',user_cookies(request))  
                return response         
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('accounts:login')
    return render(request,'accounts/login.html')

def cookies(request):
    user_cart_products = CartProduct.objects.filter(user=request.user)
    cart_data = {}
    for item in user_cart_products:
        item_data= {
        'quantity': item.quantity,
        'color':item.color,
        'size': item.size,
        }
        cart_data[str(item.product.uid)] = item_data
    return json.dumps(cart_data)


def create_user_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/register.html')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'A user with the same username or email already exists.')
        except KeyError:
            messages.error(request, 'Invalid form submission. Please try again.')
        except Exception as e:
            print(e)
    return render(request, 'accounts/register.html')

def user_profile(request):

    if request.user.is_authenticated:
        username = request.user.username
        is_authenticated = True
        cart = Cart.objects.filter(user=request.user)
        orders = Order.objects.filter(user=request.user)
        return render(request, 'accounts/profile.html', {
            'username': username,
            'is_authenticated' : is_authenticated,
            'orders' : orders,
            'cart' : cart 
        })
    else:
        is_authenticated = False
        return render(request, 'accounts/profile.html', {"is_authenticated": is_authenticated})
    


    
def logout_view(request):
    response = redirect('/home',{"is_authenticated":False})
    response.delete_cookie('cart')
    logout(request)
    return response 

def checkout(request, product_pk, product_category, product_name ):
    if request.user.is_authenticated:
        product = ['product']
        user = request.user
        product = get_object_or_404(Clothing , pk=product_pk)
        product_sizes = list(product.size.all())
        profile = get_object_or_404(User, pk=user.pk) 
        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                order_un_id = str(uuid.uuid4())
                form.save()
                messages.success(request, 'Order placed successfully!')
                return redirect('accounts:user_profile')
        else:
            form = CheckoutForm()
        return render(request, 'accounts/checkout.html', {'form': form, 'product': product})
    else:
        messages.error(request, 'You have to log in first to make orders.')
        return redirect('accounts:login')



def delete_cart_item(request,cart_pk):
    required_object = get_object_or_404(Cart, pk=cart_pk)
    required_object.delete()
    return redirect('accounts:user_profile')

def add_address(request):
    return render(request,'accounts/add-address.html')

