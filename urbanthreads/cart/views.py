from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from datetime import datetime ,timedelta
from store.models import *
import json
from accounts.models import (
    Cart,
    CartProduct
)
    
def view_cart(request):
    cart_products = []
    total_price = 0
    cookie_value = request.COOKIES.get('cart',{})
    if cookie_value :
        try:
            value_as_list = json.loads(cookie_value)
        except:
            print('no value ')
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_products = cart.cart_products.all()
            total_price = sum(product.product.product_price * product.quantity for product in cart_products)
            guest = False
            qty= None
            response = render(request, 'cart/cart.html',{'cart_products': cart_products, 'total_price': total_price,'guest':guest,'qty':qty})
            return response
    else:
        cart = request.session.get('cart', {})
        product_ids = cart.keys()
        qty = [value for value in cart.values()]
        cart_products = Clothing.objects.filter(pk__in=product_ids)
        total_price = sum(product.product_price * cart[str(product.pk)] for product in cart_products)
        guest=True
        response = render(request, 'cart/cart.html',{'cart_products': cart_products, 'total_price': total_price,'guest':guest,'qty':qty})
    return response







def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, pk=cart_product_id)
    cart_product.delete()
    return redirect('accounts:cart')
'''
I WAS HAVING A PROBLEM HERE
'''
def get_cart_data(request):
    cart_products = []
    total_price = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_products = cart.cart_products.all()
            total_price = sum(product.product.product_price * product.quantity for product in cart_products)
            guest = False
    else:
        cart = request.session.get('cart', {})
        product_ids = cart.keys()
        cart_products = Clothing.objects.filter(pk__in=product_ids)
        total_price = sum(product.product_price * cart[str(product.pk)] for product in cart_products)
        guest=True
    print(cart)
    return {'cart_products': cart_products, 'total_price': total_price,'guest':guest}



def delete_from_cart(request, product_id):
    response = redirect('cart:cart')
    if request.user.is_authenticated:
        get_object_or_404(CartProduct, pk=product_id).delete()
        response.set_cookie('cart', make_cookies(request))
    else:
        response.set_cookie('cart', make_cookies(request))
    return response

def update_cart_qty(request,product_id):
    product_id = str(product_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity is not None:
            try:
                quantity = int(quantity)
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Invalid quantity value'})

            if request.user.is_authenticated:
                cart_product = get_object_or_404(CartProduct, id=product_id, user=request.user)
                cart_product.quantity = quantity
                cart_product.save()
                response = JsonResponse({'success': True, 'message': 'Cart quantity updated'})
                response.set_cookie('cart', make_cookies(request))
            else:
                cart = request.session.get('cart', {})
                cart[str(product_id)] = quantity
                request.session['cart'] = cart
            return response

    return JsonResponse({'success': False, 'message': 'Invalid request'})

def add_to_cart_ajax(request):
    if request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Clothing, pk=product_id)
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
        response = JsonResponse({'added': True})
        cart_ = make_cookies(request)
        response.set_cookie('cart', cart_)
        return response
    else:
        cart = set_guest_cart_cookie(request)
        response = JsonResponse({'success': True})
        response.set_cookie('cart', cart)
        return response
             

def set_guest_cart_cookie(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        res = request.COOKIES.get('cart')
        if res is not None:
            res = json.loads(res)
            if res.get(product_id) is not None:
                res[product_id]['quantity'] += 1
                return json.dumps(res) 
            else:
                res[product_id]={
                'quantity': 1,
                'color': request.POST.get('color'),
                'size': request.POST.get('size')
                }
                return json.dumps(res)
        else:
            res = {}
            res[product_id]={
            'quantity': 1,
            'color': request.POST.get('color'),
            'size': request.POST.get('size')
            }
            return json.dumps(res)   

def make_cookies(request):
    user_cart_products = CartProduct.objects.filter(user=request.user)
    cart_data = {}
    for item in user_cart_products:
        print(item.product.uid)
        item_data= {
        'quantity': 1,
        'color': 'black',
        'size': 'm'
        }
        cart_data[str(item.product.uid)] = item_data
    return json.dumps(cart_data)
 