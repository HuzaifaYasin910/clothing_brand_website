from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.contrib.auth.models import User 

ORDER_STATUS = (
    ('pending','pending'),
    ('dispatched','dispatched'),
    ('canceled','canceled'),
    ('received','received')
)

class Order(models.Model):
    name    = models.CharField(max_length=100)
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
    
class Address(models.Model):
    COUNTRY_CHOICE = (
        'pakistan','pakistan'
        'australia','australia'
        'uk','uk'
        'usa','usa'
        'canada','canada'
    )
    user        = models.ForeignKey(User)
    f_name      = models.CharField(max_legth=30) 
    l_name      = models.CharField(max_legth=30)
    address     = models.TextField(max_legth=30)
    city        = models.CharField(max_legth=30)
    country     = models.CharField(choice=COUNTRY_CHOICE)
    zip_code    = models.CharField(max_length=9)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone       = models.CharField(validators=[phone_regex], max_length=17)
    email       = models.EmailField()



class Cart(models.Model):
    name    = models.CharField(max_length=100)
    pk_product = models.IntegerField()
    product_catagory = models.CharField(max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)