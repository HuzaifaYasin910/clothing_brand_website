from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from store.models import *
import uuid
from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404) 
from django.contrib.auth import (
    authenticate,
    login as auth_login
)



def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                guest_cart = request.session.get('cart', {})
                authenticated_user_cart = Cart.objects.filter(user=user).first()
                if authenticated_user_cart:
                    for product_id, quantity in guest_cart.items():
                        product = Clothing.objects.get(pk=product_id)
                        print(product.product_name)
                        cart_product, created = CartProduct.objects.get_or_create(
                            cart=authenticated_user_cart,
                            user=user,
                            product=product,
                            defaults={'quantity': quantity}
                        )
                        if not created:
                            cart_product.quantity += quantity
                            cart_product.save()
                    try:
                        del request.session['cart']
                    except:
                        cart = request.session.get('cart', {})
                    request.session.modified = True
                auth_login(request, user)
                return redirect('accounts:user_profile')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('accounts:login')
        return render(request, 'accounts/login.html')
    else:
        return redirect('accounts:user_profile')


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
    logout(request)
    return redirect('/home',{"is_authenticated":False})    




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

