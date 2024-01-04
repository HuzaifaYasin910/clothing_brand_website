from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponse
from store.models import *
import json
from accounts.models import (
    Cart,
    CartProduct
)
from .utils import make_cookies,set_guest_cart_cookie,JSONDECODE,JSONENCODE

def view_cart(request):
    cart_data = request.COOKIES.get('cart')
    if cart_data:
        items=[]
        items_data = JSONDECODE(cart_data)  
        print(items_data)
        if request.user.is_authenticated:
            
            for product_id, attributes in items_data.items():
                try:
                    product = Clothing.objects.get(pk=product_id)
                except Clothing.DoesNotExist:
                    print(f"Product with id {product_id} does not exist")
                    continue
                quantity = attributes.get('quantity',1)
                color = attributes.get('color')
                size = attributes.get('size')
                print(product)
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'color': color,
                    'size': size
                })            
        else:
            for product_id, attributes in items_data.items():
                try:
                    product = Clothing.objects.get(pk=product_id)
                except Clothing.DoesNotExist:
                    print(f"Product with id {product_id} does not exist")
                    continue

                quantity = attributes.get('quantity',1)
                color = attributes.get('color')
                size = attributes.get('size')
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'color': color,
                    'size': size
                })
        return render(request, 'cart/cart.html', {'cart_items': items})
    return render(request, 'cart/cart.html', {'cart_items': None})


def delete_from_cart(request, product_id):
    response = redirect('cart:cart')
    if request.user.is_authenticated:
        get_object_or_404(CartProduct, product=product_id).delete()
        response.set_cookie('cart', make_cookies(request))
    else:
        cart = JSONDECODE(request.COOKIES.get('cart'))
        cart.pop(product_id)
        cart = JSONENCODE(cart)
        response.set_cookie('cart', cart)
    return response

def update_cart_qty(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        product_id = (request.POST.get('product_id'))
        if request.user.is_authenticated:
            cart_product = get_object_or_404(CartProduct, product=product_id, user=request.user)
            cart_product.quantity = quantity
            cart_product.save()
            response = JsonResponse({'success': True, 'message': 'Cart quantity updated'})
            response.set_cookie('cart', make_cookies(request))
        else:
            cart = JSONDECODE(request.COOKIES.get('cart'))
            cart[product_id]['quantity']=quantity
            cart = JSONENCODE(cart)
            response = JsonResponse({'success': True, 'message': 'Cart quantity updated'})
            response.set_cookie('cart', cart)
        return response
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def add_to_cart_ajax(request):
    if request.user.is_authenticated:
        product = get_object_or_404(Clothing, pk=request.POST.get('product_id'))
        cart = Cart.objects.get_or_create(user=request.user)
        cp_created = CartProduct.objects.get_or_create(
            cart=cart,
            user=request.user,
            product=product,
            color=request.POST.get('color'),
            size=request.POST.get('size'),
            defaults={'quantity': 1}
        )
        if not cp_created:
            return JsonResponse({'added': False,'error':'Already added '})
        response = JsonResponse({'added': True})
        cart_ = make_cookies(request)
        response.set_cookie('cart', cart_)
        return response
    else:
        try:
            cart = set_guest_cart_cookie(request)
        except Exception as e:
            return JsonResponse({'added': False,'error':e})
        response = JsonResponse({'success': True})
        response.set_cookie('cart', cart)
        return response
             




 #