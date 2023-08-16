from django.db import models
import uuid
from django.contrib.auth.models import User  # Import the User model
# Create your models here.

ORDER_STATUS = (
    ('pending','pending'),
    ('dispatched','dispatched'),
    ('canceled','canceled'),
    ('received','received')
)

class Order(models.Model):
    name    = models.CharField(max_length=100)
    email   = models.EmailField()
    telephone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    post_code = models.CharField(max_length=100)
    price   = models.CharField(max_length=1000,default='0')
    product_name   = models.CharField(max_length=100)
    product_catagory    = models.CharField(max_length=1)
    product_size    = models.CharField(max_length=10)
    product_pk = models.IntegerField()
    order_un_id = models.CharField(max_length=100)
    order_status = models.CharField(max_length=10 , choices=ORDER_STATUS , default='pending')



    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    date    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order by {self.name} ' 
    

    
class Cart(models.Model):
    name    = models.CharField(max_length=100)
    pk_product = models.IntegerField()
    product_catagory = models.CharField(max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)