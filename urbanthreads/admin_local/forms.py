from django import forms
from django.forms.models import inlineformset_factory
from store.models import( 
    Clothing, 
    ClothingSize, 
    ClothingColors, 
    ClothingImages
)

class ClothingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClothingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Clothing
        fields = ['product_name', 'product_price', 'product_article', 'product_category', 'product_clothing_type']

class ClothingSizeForm(forms.ModelForm):
    class Meta:
        model = ClothingSize
        fields = ['size','quantity']
        widgets = {
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity' :forms.TextInput(attrs={'class': 'form-control'})
        }

class ClothingColorsForm(forms.ModelForm):
    class Meta:
        model = ClothingColors
        fields = ['color',]
        widgets = {
            'color' :forms.TextInput(attrs={'class': 'form-control','type':'color'}),
        }

class ClothingImagesForm(forms.ModelForm):
    class Meta:
        model = ClothingImages
        fields = ['image']
        widgets = {
            'image' :forms.FileInput(attrs={'class': 'form-control'}),
        }

ClothingColorsFormSet = inlineformset_factory(
    Clothing,
    ClothingColors,
    form=ClothingColorsForm,
    fields=('color',),
    extra=3,
    can_delete=True
)
ClothingImagesFormSet = inlineformset_factory(
    Clothing,
    ClothingImages,
    form=ClothingImagesForm,
    fields=('image',),
    extra=3,
    can_delete=True
)
ClothingSizeFormSet = inlineformset_factory(
    Clothing,
    ClothingSize,
    form=ClothingSizeForm,
    fields=('size', 'quantity'),
    extra=5,
    can_delete=True
    
)