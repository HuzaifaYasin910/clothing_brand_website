from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('user/cart',view_cart,name='cart'),
    path('add_to_cart_ajax/',add_to_cart_ajax,name='add_to_cart_ajax'),
    path('delete_from_cart/<product_id>',delete_from_cart,name='delete_from_cart'),
    path('update_cart/',update_cart_qty,name='update_cart'),
    ]