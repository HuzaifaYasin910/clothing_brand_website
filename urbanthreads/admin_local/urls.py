from django.urls import path
from .views import *
from .views import (
    create_clothing,
    update_clothing,
    delete_clothing
)

app_name = 'admin_local'

urlpatterns = [
    # Other URL patterns
    path('clothing/create/', create_clothing, name='create_clothing'),
    path('clothing/<int:pk>/update/', update_clothing, name='update_clothing'),
    path('clothing/<int:pk>/delete/', delete_clothing, name='delete_clothing'),
]
