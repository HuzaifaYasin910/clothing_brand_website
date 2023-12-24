from django import forms
from django.forms.models import inlineformset_factory
from store.models import( 
    Clothing, 
    ClothingSize, 
    ClothingColors, 
    ClothingImages
)

class ClothingForm(forms.ModelForm):
    class Meta:
        model = Clothing
        fields = ['product_name', 'product_price', 'product_article', 'product_category', 'product_clothing_type']

# Create an inline formset for ClothingSize model
ClothingSizeFormSet = inlineformset_factory(
    Clothing,
    ClothingSize,
    fields=('size', 'quantity'),
    extra=1,
    can_delete=True
    
)

# Create an inline formset for ClothingImages model
ClothingImagesFormSet = inlineformset_factory(
    Clothing,
    ClothingImages,
    fields=('image',),
    extra=1,
    can_delete=True
)

# Create an inline formset for ClothingColors model if needed
ClothingColorsFormSet = inlineformset_factory(
    Clothing,
    ClothingColors,
    fields=('color',),
    extra=1,
    can_delete=True
)