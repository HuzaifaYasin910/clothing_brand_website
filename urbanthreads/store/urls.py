from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    path('home/',home,name='home'),
    path('products/<product_category>/',product,name='products'),
    path('collection/<product_category>/<product_type>/',collection,name='collection'),
    path('product_detail/<int:product_pk>/',product_detail,name='product_detail'),
    path('error',error,name='error')

]

