# from django.contrib.auth.models import User
# from django.db import models
# from django.core.validators import MinValueValidator
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from base.models import BaseModel



# class Size(BaseModel):
#     size_name       = models.CharField(max_length=15, null=False, blank=False, default='undefined size')
#     def __str__(self):
#         return self.size_name

# class Clothing(BaseModel):
#     GENDER_CHOICES = (
#         ('M', 'M'),
#         ('W', 'W'),
#         ('B', 'B'),
#         ('G', 'G')
#     )

#     PRODUCT_TYPE = (
#     ('PANTS', 'PANTS'),
#     ('SHORTS', 'SHORTS'),
#     ('TSHIRTS', 'T-SHIRTS'),
#     ('SHIRTS', 'SHIRTS'),
#     ('TROUSERS', 'TROUSERS'),
#     ('SHOES', 'SHOES'),  
#     ('SWEATSHIRTS', 'SWEATSHIRTS'),
#     ('HOODIES', 'HOODIES'),
#     ('SWEATERS', 'SWEATERS'),
#     ('JACKETS', 'JACKETS'),
#     ('JEANS', 'JEANS'),
#     ('ACTIVEWEAR', 'ACTIVEWEAR'),
#     ('ACCESSORIES', 'ACCESSORIES'),
#     )
#     product_name    = models.CharField(max_length=30, blank=False)
#     product_price   = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
#     product_article = models.CharField(max_length=30, null=False, blank=False, unique=True, default='-------') 
#     product_category = models.CharField(max_length=1, choices=GENDER_CHOICES, default='')
#     product_clothing_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, default='')    

#     def calculate_total_quantity(self):
#         return sum(size.size_qty for size in self.product_size.all())

#     @property
#     def total_quantity(self):
#         return self.calculate_total_quantity()

#     def __str__(self):
#         return self.product_name
    
# class ClothingImages(BaseModel):
#     clothing        = models.ForeignKey(Clothing,on_delete=models.CASCADE,related_name='product_images',default=1)
#     image           = models.ImageField(null=False, upload_to='images/')

#     def __str__(self):
#         return f'Image for {self.clothing.product_name}: {self.image.url}'

# class ClothingSize(models.Model):
#     clothing        = models.ForeignKey(Clothing, on_delete=models.CASCADE,related_name='clothing_size',default=1)
#     size            = models.ForeignKey(Size, on_delete=models.CASCADE)
#     quantity        = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

#     def __str__(self):
#         return f'{self.quantity} X of {self.clothing.product_name} in {self.size} Size'

# class ClothingColors(BaseModel):
#     clothing        = models.ForeignKey(Clothing, on_delete=models.CASCADE,related_name='clothing_color',default=1)
#     color           = models.CharField(max_length=30) 

#     def __str__(self):
#         return self.color 

    