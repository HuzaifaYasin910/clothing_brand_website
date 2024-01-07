from django import forms
from .models import Order,Address  # Import the Order model (replace `.models` with your app name)

# Inside your CheckoutForm class
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)




class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ""

    COUNTRY_CHOICES = (
        ('pakistan', 'Pakistan'),
        ('australia', 'Australia'),
        ('uk', 'UK'),
        ('usa', 'USA'),
        ('canada', 'Canada'),
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-4', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-4', 'placeholder': 'Last Name'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control my-4', 'placeholder': 'Address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-4', 'placeholder': 'City'}))
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'class':'form-select my-3', 'placeholder': 'Country'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-4', 'placeholder': 'Zip Code'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control my-4', 'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-4', 'type':'tel', 'placeholder': 'Phone'}))

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'address', 'city', 'country', 'zip_code', 'email', 'phone']
        labels = {
            "comment_text": ""
        }