from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

CATAGORY = (
    ('M', 'MEN'),
    ('W', 'WOMEN'),
    ('B', 'BOYS'),
    ('G', 'GIRLS')
)

PRODUCT_TYPE = (
    ('PANTS', 'PANTS'),
    ('SHORTS', 'SHORTS'),
    ('TSHIRTS', 'T-SHIRTS'),
    ('SHIRTS', 'SHIRTS'),
    ('TROUSERS', 'TROUSERS'),
    ('SHOES', 'SHOES'),
    
)



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

class Adult_size(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False, default='undefined size')

    def __str__(self):
        return self.name

class Minor_size(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False, default='undefined size')

    def __str__(self):
        return self.name



class Men(models.Model):
    image = models.ImageField(null=False, upload_to='m_images/')
    name = models.CharField(max_length=30, blank=False)
    price = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    article = models.CharField(max_length=30, null=False, blank=False, unique=True, default='-------')
    size = models.ManyToManyField(Adult_size)
    qty = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    color = models.CharField(max_length=30, blank=True, default='None')
    catagory = models.CharField(max_length=1, default='M', choices=CATAGORY)
    product_type  = models.CharField(max_length=8,choices=PRODUCT_TYPE)

    def __str__(self):
        return self.name

class Women(models.Model):    
    image   = models.ImageField(null=False,upload_to='w_images/')
    name    = models.CharField(max_length=30, blank=False)
    price   = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    article = models.CharField(max_length=30,null=False,blank=False,unique=True,default='-------')
    size = models.ManyToManyField(Adult_size)
    qty     = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    color   = models.CharField(max_length=30, blank=True, default='None')
    catagory = models.CharField(max_length=1,default='W',choices=CATAGORY)
    product_type  = models.CharField(max_length=8,choices=PRODUCT_TYPE)
    def __str__(self):
        return  self.name
    

       
class Boys(models.Model):
    image   = models.ImageField(null=False,upload_to='b_images/')
    name    = models.CharField(max_length=30, blank=False)
    price   = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    article = models.CharField(max_length=30,null=False,blank=False,unique=True,default='-------')
    size    = models.ManyToManyField(Minor_size)
    qty     = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    color   = models.CharField(max_length=30, blank=True, default='None')
    catagory  = models.CharField(max_length=1,default='B',choices=CATAGORY)
    def __str__(self):
        return  self.name


class Girls(models.Model):
    image   = models.ImageField(null=False,upload_to='g_images/')
    name    = models.CharField(max_length=30, blank=False)
    price   = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    article = models.CharField(max_length=30,null=False,blank=False,unique=True,default='-------')
    size    = models.ManyToManyField(Minor_size)
    qty     = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    color   = models.CharField(max_length=30, blank=True, default='None')
    catagory  = models.CharField(max_length=1,default='G',choices=CATAGORY)
    


    def __str__(self):
        return  self.name
    




