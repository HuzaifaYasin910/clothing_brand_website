from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType




class Size(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False, default='undefined size')
    def __str__(self):
        return self.name



class Clothing(models.Model):
    GENDER_CHOICES = (
        ('M', 'M'),
        ('W', 'W'),
        ('B', 'B'),
        ('G', 'G')
    )

    AGE_GROUP_CHOICES = (
        ('A', 'Adult'),
        ('M', 'Minor'),
    )

    PRODUCT_TYPE = (
    ('PANTS', 'PANTS'),
    ('SHORTS', 'SHORTS'),
    ('TSHIRTS', 'T-SHIRTS'),
    ('SHIRTS', 'SHIRTS'),
    ('TROUSERS', 'TROUSERS'),
    ('SHOES', 'SHOES'),  
    )

    image = models.ImageField(null=False, upload_to='products_images/')
    name = models.CharField(max_length=30, blank=False)
    price = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    article = models.CharField(max_length=30, null=False, blank=False, unique=True, default='-------')
    size = models.ManyToManyField(Size)  
    qty = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    color = models.CharField(max_length=30, blank=True, default='None')
    category = models.CharField(max_length=1, choices=GENDER_CHOICES, default='')
    age_group = models.CharField(max_length=1, choices=AGE_GROUP_CHOICES, default='')
    clothing_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, default='')

    def content_file_name(self, filename):
        ext = filename.split('.')[-1]
        return '/'.join(['uploads', self.name, filename])

    def __str__(self):
        return self.name
    


class ClothingSizeQuantity(models.Model):
    clothing = models.ForeignKey(Clothing, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('clothing', 'size',)

    def __str__(self):
        return f"{self.clothing.name} - {self.size.name} - Qty: {self.quantity}"