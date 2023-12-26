from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from store.models import *
from accounts.models import (
    Cart,
    CartProduct
)



    



def cart(request):
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
    return render(request, 'accounts/cart.html', {'cart_products': cart_products, 'total_price': total_price,'guest':guest})



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

    return redirect('store:home')

@login_required
def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, pk=cart_product_id)
    cart_product.delete()
    return redirect('view_cart')