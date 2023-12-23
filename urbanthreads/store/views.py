from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
# Create your views here.

def home(request):
    return render(request, 'store/home.html')


def product(request, product_category):
    try:
        products = Clothing.objects.filter(category=product_category)
        if not products.exists():
            raise Clothing.DoesNotExist("No products found for the given category.")
        return render(request, 'store/product_list.html', {"products": products})
    except Clothing.DoesNotExist as e:
        print(f"Error: {e}")
        return render(request, 'store/error.html', {"error_message": "Category not found."})
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'store/error.html', {"error_message": "An error occurred."})

def collection(request, product_type,product_category):
    products = Clothing.objects.filter(product_category=product_category,clothing_type=product_type)
    return render(request, 'store/product_list.html', {"products": products})

def product_detail(request , product_pk):   
    try:
        product = get_object_or_404(Clothing, pk=product_pk)
        return render(request, 'store/product-page.html', {
            'product': product,
        })
    except Exception as e:
        print('################### error - product detail ###################')
        print(f"Error: {e}")
        return render(request, 'store/error.html', {"error_message": "Category not found."})

def error(request):
    return render(request, 'store/error.html')