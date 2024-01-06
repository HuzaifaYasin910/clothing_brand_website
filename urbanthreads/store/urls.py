from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    path('home/',home,name='home'),
    path('about_us',about_us,name='about_us'),
    path('products/<product_category>/',product,name='products'),
    path('collection/<product_category>/<product_type>/',collection,name='collection'),
    path('product_detail/<product_id>/',product_detail,name='product_detail'),
    path('error',error,name='error')

]

