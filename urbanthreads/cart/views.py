from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from store.models import *
from accounts.models import (
    Cart,
    CartProduct
)



    





def cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_products = cart.cart_products.all()
    return render(request,'accounts/cart.html',{'cart': cart, 'cart_products': cart_products})
 
@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Clothing, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_product, cp_created = CartProduct.objects.get_or_create(
        cart=cart,
        user=user,  # Set the user attribute
        product=product,
        defaults={'quantity': 1} 
    )
    if not cp_created:
        cart_product.quantity += 1
        cart_product.save()

    return redirect('accounts:user_profile')    

@login_required
def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, pk=cart_product_id)
    cart_product.delete()
    return redirect('view_cart')