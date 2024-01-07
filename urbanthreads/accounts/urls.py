from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/',create_user_account,name='signup'),
    path('user/profile/',user_profile,name='user_profile'),
    path('logout/', logout_view, name='logout'),
    path('cart-item/<int:cart_pk>', delete_cart_item, name='cart_item'),
    path('checkout/<product_pk>/<product_category>/<product_name>/', checkout, name='checkout'),
    path('user/addresses/',view_addresses,name='view_addresses'),
    path('user/add-address',add_address,name='add_address'),
    path('user/delete-address/<address_pk>/',delete_address,name='delete_address'),
    ]