from django.urls import path
from .views import *

app_name = 'admin_local'

urlpatterns = [
    path('admin_local/',admin_local_portal,name='admin_local'),
    path('order_detail/<int:order_pk>',order_detail,name='order_detail'),


]