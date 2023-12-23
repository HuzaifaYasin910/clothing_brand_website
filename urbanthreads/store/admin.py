from django.contrib import admin
from .models import (
    Size,
    Clothing,
    ClothingSizeQuantity,
    ClothingImages
)


# Register your models here.
admin.site.register(Size)

class ClothingImagesAdmin(admin.StackedInline):
    model = ClothingImages

class ClothingAdmin(admin.ModelAdmin):
    inlines = [ClothingImagesAdmin]

admin.site.register(Clothing,ClothingAdmin)

admin.site.register(ClothingImages)
admin.site.register(ClothingSizeQuantity)