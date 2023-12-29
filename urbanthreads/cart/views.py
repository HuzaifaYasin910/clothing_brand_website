from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import *
from accounts.models import (
    Cart,
    CartProduct
)
    
def view_cart(request):
    cart_products = []
    total_price = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_products = cart.cart_products.all()
            total_price = sum(product.product.product_price * product.quantity for product in cart_products)
            guest = False
            qty= None
    else:
        cart = request.session.get('cart', {})
        product_ids = cart.keys()
        qty = [value for value in cart.values()]
        cart_products = Clothing.objects.filter(pk__in=product_ids)
        total_price = sum(product.product_price * cart[str(product.pk)] for product in cart_products)
        guest=True
    return render(request, 'cart/cart.html',{'cart_products': cart_products, 'total_price': total_price,'guest':guest,'qty':qty})

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

def delete_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart_product = get_object_or_404(CartProduct, pk=product_id)
        cart_product.delete()
    else:

        guest_cart = request.session.get('cart', {})

        if str(product_id) in guest_cart:
            del guest_cart[str(product_id)]  
            request.session['cart'] = guest_cart 
            request.session.modified = True  

    return redirect('cart:cart')

def update_cart_qty(request,product_id):
    product_id = str(product_id)
    if request.method == 'POST':
        print('received in guest')
        quantity = request.POST.get('quantity')
        if quantity is not None:
            try:
                quantity = int(quantity)
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Invalid quantity value'})

            if request.user.is_authenticated:
                print('received in user')
                cart_product = get_object_or_404(CartProduct, id=product_id, user=request.user)
                cart_product.quantity = quantity
                cart_product.save()
            else:
                print('received in guest')
                # For non-authenticated users, handle quantity update in session
                cart = request.session.get('cart', {})
                cart[str(product_id)] = quantity
                request.session['cart'] = cart

            return JsonResponse({'success': True, 'message': 'Cart quantity updated'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})