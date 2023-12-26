from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import *
from accounts.models import (
    Cart,
    CartProduct
)



    
def cart(request):
    return render(request, 'accounts/cart.html')



def add_to_cart(request, product_id):
    product = get_object_or_404(Clothing, pk=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_product, cp_created = CartProduct.objects.get_or_create(
            cart=cart,
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not cp_created:
            cart_product.quantity += 1
            cart_product.save()
    else:
        cart = request.session.get('cart', {})
        cart_product_quantity = cart.get(str(product_id), 0)
        cart[str(product_id)] = cart_product_quantity + 1
        request.session['cart'] = cart
    return redirect('accounts:cart')

def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, pk=cart_product_id)
    cart_product.delete()
    return redirect('accounts:cart')



def add_to_cart_ajax(request, product_id):
    product = get_object_or_404(Clothing, pk=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_product, cp_created = CartProduct.objects.get_or_create(
            cart=cart,
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not cp_created:
            cart_product.quantity += 1
            cart_product.save()
    else:
        cart = request.session.get('cart', {})
        cart_product_quantity = cart.get(str(product_id), 0)
        cart[str(product_id)] = cart_product_quantity + 1
        request.session['cart'] = cart
    response_data = {'added': True}
    return JsonResponse(response_data)