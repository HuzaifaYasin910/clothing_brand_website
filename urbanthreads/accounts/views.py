from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login as auth_login
from store.models import *
from django.db import transaction
import uuid

def login_view(request):
    """
    Handles the login functionality.

    Attempts to authenticate the user using the provided credentials.
    If successful, the user is logged in and redirected to the user_profile page.
    If unsuccessful, an error message is displayed and the user is redirected back to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered login page template or redirect to user_profile page if authenticated.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user) 
            return redirect('accounts:user_profile')  
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')


def create_user_account(request):
    """
    Creates a new user account.

    Attempts to create a new user account using the provided username, email, and password.
    If successful, a success message is displayed, and the user is redirected to the login page.
    If any error occurs (e.g., missing fields, duplicate username or email), appropriate error messages are displayed.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered register page template or redirect to login page if account created successfully.
    """
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
    """
    Renders the user profile page.

    If the user is authenticated, their profile details, order history, and cart items are displayed.
    If the user is not authenticated, only the authentication status is displayed.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered profile page template with user details, orders, and cart items or authentication status.
    """
    if request.user.is_authenticated:
       
        username = request.user.username
        email = request.user.email
        is_authenticated = True
        cart = Cart.objects.filter(user=request.user)
        orders = Order.objects.filter(user=request.user)
        return render(request, 'accounts/profile.html', {
            'username': username,
            'email': email,
            'is_authenticated': is_authenticated,
            'orders': orders,
            'cart':cart 
        })
    else:
        is_authenticated = False
        return render(request, 'accounts/profile.html', {"is_authenticated": is_authenticated})
    


    
def logout_view(request):
    """
    Logs out the user.

    Logs out the currently authenticated user and redirects to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirect to the home page.
    """
    logout(request)
    return redirect('/home',{"is_authenticated":False})    


def checkout(request, product_pk, product_catagory, product_name, product_price):
    """
    Handles the checkout process for placing orders.

    Validates the order form and saves the order details to the database.
    Also, updates the product quantity after placing the order.

    Args:
        request (HttpRequest): The HTTP request object.
        product_pk (int): The primary key of the product being ordered.
        product_category (str): The product category code ('M' for Men, 'W' for Women).
        product_name (str): The name of the product being ordered.
        product_price (float): The price of the product being ordered.

    Returns:
        HttpResponse: Rendered checkout page template with the order form or redirects to user_profile page on successful order placement.
    """
    if request.user.is_authenticated:
        check = qty_check(product_pk, product_catagory)
        is_available = check['is_available']
        product = check['product']
        user = request.user
        product = product_check(product_pk, product_catagory)
        profile = get_object_or_404(User, pk=user.pk) 
        if request.method == 'POST' and is_available:
            form = CheckoutForm(request.POST)
            if form.is_valid():
                order_un_id = str(uuid.uuid4())
                new_order = Order(
                    order_un_id=order_un_id, 
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    telephone=form.cleaned_data['telephone'],
                    address=form.cleaned_data['address'],
                    post_code=form.cleaned_data['post_code'],
                    product_size=form.cleaned_data['product_size'],
                    price=product_price,
                    product_name=product_name,
                    product_catagory=product_catagory,
                    product_pk=product_pk,
                    user=profile
                )
                new_order.save()
                with transaction.atomic():
                    product.qty -= 1
                    product.save()
                messages.success(request, 'Order placed successfully!')
                return redirect('accounts:user_profile')
        else:
            form = CheckoutForm(initial={
                'product_catagory': product_catagory,
                'product_pk': product_pk,
                'product_name': product_name,
                'price': product_price
            })
        return render(request, 'accounts/checkout.html', {'form':form,'product':product,})
    else:
        messages.error(request, 'You have to log in first to make orders.')
        return redirect('accounts:login')





def qty_check(product_pk, product_catagory):
    """
    Checks if the product quantity is available.

    Determines if the product quantity for the specified product and category is greater than or equal to 1.

    Args:
        product_pk (int): The primary key of the product.
        product_category (str): The product category code ('M' for Men, 'W' for Women, 'B' for Boys, 'G' for Girls).

    Returns:
        dict: A dictionary with the keys 'is_available' (bool) and 'product' (Product object).
    """
    if product_catagory == 'M':
        product = get_object_or_404(Men, pk=product_pk)
    elif product_catagory == 'W':
        product = get_object_or_404(Women, pk=product_pk)    
    elif product_catagory == 'B':
        product = get_object_or_404(Boys, pk=product_pk) 
    elif product_catagory == 'G':        
        product = get_object_or_404(Girls, pk=product_pk) 
    else:
        return redirect('store:error')
    is_available = product.qty >= 1
    return {'is_available': is_available, 'product': product}


def cart(request,product_pk,product_catagory,product_name):
    """
    Adds a product to the cart for the authenticated user.

    Creates a new Cart object for the user with the specified product details.

    Args:
        request (HttpRequest): The HTTP request object.
        product_pk (int): The primary key of the product being added to the cart.
        product_category (str): The product category code ('M' for Men, 'W' for Women, 'B' for Boys, 'G' for Girls).
        product_name (str): The name of the product being added to the cart.

    Returns:
        HttpResponse: Redirect to the user_profile page on successful cart item addition or to the login page if the user is not authenticated.
    """
    if request.user.is_authenticated:
        user = request.user
        if product_catagory == 'M':
            new_object = Cart.objects.create(name=product_name,pk_product=product_pk, product_catagory=product_catagory,user=user)
        elif product_catagory == 'W':
            new_object = Cart.objects.create(name=product_name,pk_product=product_pk, product_catagory=product_catagory,user=user)
        elif product_catagory == 'B':
            product = get_object_or_404(Boys, pk=product_pk)
            new_object = Cart.objects.create(name=product_name,pk_product=product_pk, product_catagory=product_catagory,user=user)
        elif product_catagory == 'G':
            product = get_object_or_404(Girls, pk=product_pk)
            new_object = Cart.objects.create(name=product_name,pk_product=product_pk, product_catagory=product_catagory,user=user)
        else:
            return redirect('store:error')
        return redirect('accounts:user_profile')
    else:
        messages.success(request, 'You have to login first to make orders/add to cart.')
        return redirect('accounts:login')
    

def delete_cart_item(request,cart_pk):
    """
    Deletes a cart item from the user's cart.

    Deletes the cart item with the specified primary key from the user's cart.

    Args:
        request (HttpRequest): The HTTP request object.
        cart_pk (int): The primary key of the cart item to delete.

    Returns:
        HttpResponse: Redirect to the user_profile page after deleting the cart item.
    """
    get_object_or_404(Cart, pk=cart_pk).delete()
    return redirect('accounts:user_profile')


def product_check(product_pk, product_catagory):
    """
    Checks and retrieves the product from the database.

    Retrieves the product object based on the given product primary key and category.

    Args:
        product_pk (int): The primary key of the product.
        product_category (str): The product category code ('M' for Men, 'W' for Women, 'B' for Boys, 'G' for Girls).

    Returns:
        Product: The product object retrieved from the database.
    """
    product_model = None
    if product_catagory == 'M':
        product_model = Men
    elif product_catagory == 'W':
        product_model = Women
    elif product_catagory == 'B':
        product_model = Boys
    elif product_catagory == 'G':
        product_model = Girls
    else:
        return redirect('store:error')
    product = get_object_or_404(product_model, pk=product_pk)
    return product