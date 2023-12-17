from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType




class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # GenericForeignKey fields to link to different product models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    post = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Review by {self.user.username} on {self.post}"

class sizes(models.Model):
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
    size = models.ManyToManyField(sizes)  
    qty = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    color = models.CharField(max_length=30, blank=True, default='None')
    category = models.CharField(max_length=1, choices=GENDER_CHOICES, default='')
    age_group = models.CharField(max_length=1, choices=AGE_GROUP_CHOICES, default='')
    clothing_type = models.CharField(max_length=20, choices=PRODUCT_TYPE, default='')

    def content_file_name(self, filename):
        ext = filename.split('.')[-1]
        return '/'.join(['uploads', self.Clothing.name, filename])

    def __str__(self):
        return self.name