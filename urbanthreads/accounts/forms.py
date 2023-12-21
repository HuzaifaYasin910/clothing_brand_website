from django import forms
from .models import Order  # Import the Order model (replace `.models` with your app name)

# Inside your CheckoutForm class
class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, product_sizes=None, **kwargs):
        self.product_sizes = product_sizes  # Store product_sizes within the form
        super(CheckoutForm, self).__init__(*args, **kwargs)

    # ... Rest of your form definition

        self.fields['product_size'].widget = forms.Select(choices=[(size, size) for size in product_sizes ], attrs={'class': 'form-control'})

    class Meta:
        model = Order
        fields = ('name', 'address', 'email', 'telephone', 'post_code', 'product_size')

    name        = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address     = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email       = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone   = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    post_code   = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_size = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}))