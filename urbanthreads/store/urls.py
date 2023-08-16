from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    path('home/',home,name='home'),
    path('about/',about,name='about'),
    path('products/<int:product_category>/',product,name='products'),
    path('collection/<str:product_category>/<str:product_type>/',collection,name='collection'),
    path('product_detail/<str:product_category>/<int:product_pk>/',product_detail,name='product_detail'),
    path('error',error,name='error')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)