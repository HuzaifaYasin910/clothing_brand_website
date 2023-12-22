from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.contrib.auth.models import User 
from store.models import Clothing


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'PENDING'),
        ('dispatched', 'DISPATCHED'),
        ('canceled', 'CANCELED'),
        ('received', 'RECEIVED')
    )
    name            = models.CharField(max_length=100)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    price           = models.CharField(max_length=1000,default='0')
    product         = models.ForeignKey(Clothing, on_delete=models.CASCADE)
    order_un_id     = models.CharField(max_length=100)
    order_status    = models.CharField(max_length=10 , choices=ORDER_STATUS , default='pending')
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    date            = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order by {self.name} ' 

class Address(models.Model):
    COUNTRY_CHOICES = (
        ('pakistan', 'Pakistan'),
        ('australia', 'Australia'),
        ('uk', 'UK'),
        ('usa', 'USA'),
        ('canada', 'Canada'),
    )
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    address         = models.TextField(max_length=100)
    city            = models.CharField(max_length=30)
    country         = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    zip_code        = models.CharField(max_length=9)
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone           = models.CharField(validators=[phone_regex], max_length=17)
    email           = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} from {self.city} , {self.country}'
    

class CartProduct(models.Model):
    refering_cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Clothing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart.name}'s {self.product.name} x {self.quantity}"



class Cart(models.Model):
    name            = models.CharField(max_length=100)
    products        = models.ManyToManyField(Clothing)
    cart_products = models.ManyToManyField(CartProduct)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)