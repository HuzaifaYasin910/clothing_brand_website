from django import forms
from .models import Order

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=100)
    email = forms.EmailField()
    telephone = forms.CharField(max_length=30)
    post_code = forms.CharField(max_length=20)
    product_size    = forms.CharField(max_length=10)