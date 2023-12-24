from django.http import HttpResponse
from accounts.models import Order
from django.db.models import Q
from store.models import *
from .forms import ClothingForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.views.generic.edit import (
    CreateView,
    UpdateView
)
from .forms import (
    ClothingForm, 
    ClothingSizeFormSet, 
    ClothingImagesFormSet,
    ClothingColorsFormSet
)
from store.models import( 
    Clothing, 
    ClothingSize, 
    ClothingColors, 
    ClothingImages
)


from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, redirect
from .forms import ClothingForm, ClothingSizeFormSet, ClothingImagesFormSet, ClothingColorsFormSet

def create_clothing(request):
    if request.method == 'POST':
        clothing_form = ClothingForm(request.POST)
        size_formset = ClothingSizeFormSet(request.POST, prefix='size')
        images_formset = ClothingImagesFormSet(request.POST, request.FILES, prefix='images')
        colors_formset = ClothingColorsFormSet(request.POST, prefix='colors')

        if clothing_form.is_valid() and size_formset.is_valid() and images_formset.is_valid() and colors_formset.is_valid():
            clothing = clothing_form.save()
            # Save the sizes
            if size_formset.is_valid():
               
                size_formset.instance = clothing
                size_formset.save()

            # Save the images
            if images_formset.is_valid():
               
                images_formset.instance = clothing
                images_formset.save()

            # Save the colors
            if colors_formset.is_valid():
                for x in size_formset:
                    print(x)
                colors_formset.instance = clothing
                colors_formset.save()

            return redirect('clothing_detail', pk=clothing.pk)
    else:
        clothing_form = ClothingForm()
        size_formset = ClothingSizeFormSet(prefix='size')
        images_formset = ClothingImagesFormSet(prefix='images')
        colors_formset = ClothingColorsFormSet(prefix='colors')

    return render(request, 'admin_local/create.html', {
        'size_formset_count': size_formset.total_form_count,
        'images_formset_count': images_formset.total_form_count,
        'colors_formset_count': colors_formset.total_form_count,
        'clothing_form': clothing_form,
        'size_formset': size_formset,
        'images_formset': images_formset,
        'colors_formset': colors_formset,
    })


def update_clothing(request, pk):
    clothing = get_object_or_404(Clothing, pk=pk)
    if request.method == 'POST':
        clothing_form = ClothingForm(request.POST, instance=clothing)
        size_formset = ClothingSizeFormSet(request.POST, instance=clothing, prefix='size')
        images_formset = ClothingImagesFormSet(request.POST, request.FILES, instance=clothing, prefix='images')
        colors_formset = ClothingColorsFormSet(request.POST, instance=clothing, prefix='colors')

        if clothing_form.is_valid() and size_formset.is_valid() and images_formset.is_valid() and colors_formset.is_valid():
            clothing = clothing_form.save()

            size_formset.save()
            images_formset.save()
            colors_formset.save()

            return redirect('clothing_detail', pk=clothing.pk)
    else:
        clothing_form = ClothingForm(instance=clothing)
        size_formset = ClothingSizeFormSet(instance=clothing, prefix='size')
        images_formset = ClothingImagesFormSet(instance=clothing, prefix='images')
        colors_formset = ClothingColorsFormSet(instance=clothing, prefix='colors')

    return render(request, 'admin_local/update.html', {
        'clothing_form': clothing_form,
        'size_formset': size_formset,
        'images_formset': images_formset,
        'colors_formset': colors_formset,
    })

def delete_clothing(request, pk):
    clothing = get_object_or_404(Clothing, pk=pk)
    if request.method == 'POST':
        clothing.delete()
        return redirect('clothing_list')
    
    return render(request, 'admin_local/delete.html', {'clothing': clothing})
