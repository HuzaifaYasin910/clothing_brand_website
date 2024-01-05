from cart.utils import JSONDECODE,JSONENCODE
from .models import Clothing,CartProduct,Cart
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

def process_guest_cookies(request,cookie_cart,user):
        items_data = JSONDECODE(cookie_cart)
        user_cart, created = Cart.objects.get_or_create(user=user)
        new_cart_products = []
        for product_id, attributes in items_data.items():
            try:
                product = Clothing.objects.get(pk=attributes['product'])
            except Clothing.DoesNotExist:
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
        try:
            CartProduct.objects.bulk_create(new_cart_products)
        except Exception as e:
             logger.error(e)