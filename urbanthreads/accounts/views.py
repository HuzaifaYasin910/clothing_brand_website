from django.contrib.auth.models import User
from django.db.models import F
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
from .models import *
from store.models import Clothing
from cart.utils import helper_cookies,JSONDECODE,JSONENCODE
from django.http import HttpResponse
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
from cart.views import make_cookies

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))    
        if user :
            cart = request.COOKIES.get('cart')
            if cart:
                try: items_data = json.loads(cart)
                except Exception as e:return HttpResponse('error in handeling of json data',e)
                user_cart, created = Cart.objects.get_or_create(user=user)   
                cart_products = CartProduct.objects.filter(
                    cart=user_cart,
                    user=user
                ).select_related('product')
                new_cart_products=[]
                existing_products = {cp.product_id: cp for cp in cart_products}
                print(existing_products,'existing_products')
                for product_id, attributes in items_data.items():
                    

                    existing_cart_product = existing_products.get(product_id)

                    if existing_cart_product:
                        print(f"Product with id {product_id} already exists")
                        continue
                    try:
                        product = Clothing.objects.get(pk=product_id)
                    except Clothing.DoesNotExist:
                        print(f"Product with id {product_id} does not exist")
                        continue
                    
                    quantity = attributes.get('quantity', 1)
                    color = attributes.get('color')
                    size = attributes.get('size')

                    new_cart_products.append(
                        CartProduct(
                            user=user,
                            product=product,
                            quantity=quantity,
                            color=color,
                            size=size,
                            cart=user_cart
                        )
                    )

                # Bulk create new products if new_cart_products is not empty
                if new_cart_products:
                    CartProduct.objects.bulk_create(new_cart_products)

                auth_login(request, user)
                response = redirect('accounts:user_profile')
                response.set_cookie('cart',make_cookies(request))
                return response
                            
            else:
                print('none cart')
                auth_login(request, user)
                response = redirect('accounts:user_profile')
                response.set_cookie('cart',make_cookies(request))
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

