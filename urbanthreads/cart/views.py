from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponse
from store.models import *
import json
from accounts.models import (
    Cart,
    CartProduct
)
import logging
from .utils import user_cookies,guest_cookies,JSONDECODE,JSONENCODE
from django.db import IntegrityError
logger = logging.getLogger(__name__)
def view_cart(request):
    cookie_cart = request.COOKIES.get('cart')
    if cookie_cart:
        items=[]
        items_data = JSONDECODE(cookie_cart)
        for key, attributes in items_data.items():
            product_uid = attributes.get('product')
            try:
                product = Clothing.objects.get(pk=product_uid)
            except Clothing.DoesNotExist:continue
            items.append({
                'product': product,
                'quantity': attributes.get('quantity'),
                'color': attributes.get('color'),
                'size': attributes.get('size'),
                'key':key
            })
        return render(request, 'cart/cart.html', {'cart_items': items,})
    return render(request, 'cart/cart.html', {'cart_items': None})



def delete_from_cart(request, product_id):
    response = redirect('cart:cart')
    if request.user.is_authenticated:
        get_object_or_404(
            CartProduct,
                pk=product_id,
                ).delete()
        response.set_cookie('cart', user_cookies(request))
    else:
        cart = JSONDECODE(request.COOKIES.get('cart'))
        cart.pop(product_id)
        cart = JSONENCODE(cart)
        response.set_cookie('cart', cart)
    return response

def update_cart_qty(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cookie_cart = request.COOKIES.get('cart')
            cookie_cart  = JSONDECODE(cookie_cart)
            index = request.POST.get('product_id')
            cart_products = CartProduct.objects.filter(
                pk=index,
                user=request.user
                )
            cart_products.update(quantity=request.POST.get('quantity'))
            response = JsonResponse({'success': True, 'message': 'Cart quantity updated'})
            response.set_cookie('cart', user_cookies(request))
        else:
            cart = JSONDECODE(request.COOKIES.get('cart'))
            cart[request.POST.get('product_id')]['quantity']=request.POST.get('quantity')
            cart = JSONENCODE(cart)
            response = JsonResponse({'success': True, 'message': 'Cart quantity updated'})
            response.set_cookie('cart', cart)
        return response
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def add_to_cart_ajax(request):
    if request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        color = request.POST.get('color')
        size = request.POST.get('size')
        cookie_cart = request.COOKIES.get('cart', {})
        cookie_cart = JSONDECODE(cookie_cart)
        if product_id in [value['product'] for value in cookie_cart.values() if value['product'] == product_id and value['color'] == color and value['size'] == size]:
            return JsonResponse({'added': False, 'error': 'Already added'})
        else:
            product = get_object_or_404(Clothing, pk=product_id)
            cart, cart_created = Cart.objects.get_or_create(user=request.user)
            CartProduct.objects.create(
                cart=cart,
                user=request.user,
                product=product,
                color=color,
                size=size,
                quantity=1
            )
            response = JsonResponse({'added': True})
            cart_ = user_cookies(request)
            response.set_cookie('cart', cart_)
            return response

    else:
        try:
            cart = guest_cookies(request)
        except Exception as e:
            return JsonResponse({'added': False, 'error': e})

        response = JsonResponse({'success': True})
        response.set_cookie('cart', cart)
        return response
