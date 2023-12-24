from django.contrib import admin
from .models import (
    ClothingSize,
    Clothing,
    ClothingImages,
    ClothingColors
)
# Register your models here.

class ClothingImagesAdmin(admin.StackedInline):
    model = ClothingImages

class ClothingColorsAdmin(admin.StackedInline):
    model = ClothingColors

class ClothingSizeAdmin(admin.StackedInline):
    model = ClothingSize

class ClothingAdmin(admin.ModelAdmin):
    inlines = [ClothingImagesAdmin, ClothingColorsAdmin, ClothingSizeAdmin]

admin.site.register(Clothing,ClothingAdmin)

admin.site.register(ClothingImages)

@admin.register(ClothingColors)
class ClothingColorsAdmin(admin.ModelAdmin):
    model = ClothingColors