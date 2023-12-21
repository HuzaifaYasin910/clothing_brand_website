from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/',create_user_account,name='signup'),
    path('user_profile/',user_profile,name='user_profile'),
    path('logout/', logout_view, name='logout'),
    path('cart/<int:product_pk>/<str:product_catagory>/<str:product_name>/', cart, name='cart'),
    path('cart_item/<int:cart_pk>', delete_cart_item, name='cart_item'),
    path('checkout/<product_pk>/<product_category>/<product_name>/', checkout, name='checkout'),
]