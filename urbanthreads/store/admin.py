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

@admin.register(ClothingColors)
class ClothingColorsAdmin(admin.ModelAdmin):
    model = ClothingColors

class ClothingAdmin(admin.ModelAdmin):
    inlines = [ClothingImagesAdmin]



admin.site.register(Clothing,ClothingAdmin)

admin.site.register(ClothingImages)