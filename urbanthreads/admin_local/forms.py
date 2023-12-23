from django import forms
from store.models import Clothing, ClothingSize, ClothingColors ,ClothingImages
from django.forms.models import inlineformset_factory

class ClothingForm(forms.ModelForm):
    product_name = forms.CharField(max_length=30)
    product_name = forms.CharField(max_length=30)
    product_name = forms.CharField(max_length=30)
    product_name = forms.CharField(max_length=30)
    product_name = forms.CharField(max_length=30)
    product_name = forms.CharField(max_length=30)
    
    class Meta:
        model = Clothing
        fields = ['product_name', 'product_price', 'product_article', 'product_category', 'product_clothing_type']

