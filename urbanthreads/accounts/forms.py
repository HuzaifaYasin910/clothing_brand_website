from django import forms
from .models import Order  # Import the Order model (replace `.models` with your app name)

# Inside your CheckoutForm class
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
