from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from base.models import BaseModel



class Size(BaseModel):
    name = models.CharField(max_length=15, null=False, blank=False, default='undefined size')
    def __str__(self):
        return self.name



class Clothing(BaseModel):
    GENDER_CHOICES = (
        ('M', 'M'),
        ('W', 'W'),
        ('B', 'B'),
        ('G', 'G')
    )
    PRODUCT_TYPE = (
    ('PANTS', 'PANTS'),
    ('SHORTS', 'SHORTS'),
    ('TSHIRTS', 'T-SHIRTS'),
    ('SHIRTS', 'SHIRTS'),
    ('TROUSERS', 'TROUSERS'),
    ('SHOES', 'SHOES'),  
    ('SWEATSHIRTS', 'SWEATSHIRTS'),
    ('HOODIES', 'HOODIES'),
    ('SWEATERS', 'SWEATERS'),
    ('JACKETS', 'JACKETS'),
    ('JEANS', 'JEANS'),
    ('ACTIVEWEAR', 'ACTIVEWEAR'),
    ('ACCESSORIES', 'ACCESSORIES'),
    )
    product_name    = models.CharField(max_length=30, blank=False)
    product_price   = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    product_article = models.CharField(max_length=30, null=False, blank=False, unique=True, default='-------')
    product_size    = models.ManyToManyField(Size)  
    product_qty     = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    product_color   = models.CharField(max_length=30, blank=True, default='None')
    product_category = models.CharField(max_length=1, choices=GENDER_CHOICES, default='')
    product_clothing_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, default='')

    def content_file_name(self, filename):
        ext = filename.split('.')[-1]
        return '/'.join(['uploads', self.uid])

    def __str__(self):
        return self.product_name
    
class ClothingImages(BaseModel):
    clothing        = models.ForeignKey(Clothing,on_delete=models.CASCADE,related_name='product_images')
    image           = models.ImageField(null=False, upload_to='products_images/')

class ClothingSizeQuantity(BaseModel):
    clothing = models.ForeignKey(Clothing, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('clothing', 'size',)

    def __str__(self):
        return f"{self.clothing.name} - {self.size.name} - Qty: {self.quantity}"