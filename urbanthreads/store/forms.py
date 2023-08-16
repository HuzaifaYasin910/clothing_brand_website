# forms.py

from django import forms
from .models import Reviews

class CommentForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['text']

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    email = forms.EmailField()
    telephone = forms.CharField(max_length=100)
    post_code = forms.CharField(max_length=100)