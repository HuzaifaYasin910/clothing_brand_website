from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('cart/<int:product_pk>/<str:product_catagory>/<str:product_name>/', cart, name='cart'),
    path('user/cart',cart,name='cart'),
    path('add_to_cart/<product_id>',add_to_cart,name='add_to_cart'),
    path('add_to_cart_ajax/<product_id>',add_to_cart_ajax,name='add_to_cart_ajax'),
    ]