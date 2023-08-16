from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
# Create your views here.

def home(request):
    """
    Renders the home page of the store.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered home page template.
    """
    return render(request, 'store/home.html')


def about(request):
    """
    Renders the about page of the store.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered about page template.
    """
    return render(request, 'store/about.html')


def product(request, product_category):
    """
    Renders a list of products based on the given product category.

    Args:
        request (HttpRequest): The HTTP request object.
        product_category (int): The product category identifier.

    Returns:
        HttpResponse: Rendered product list template or redirects to the error page if invalid category.
    """
    try:
        if product_category == 1:
            products = Men.objects.all()
        elif product_category == 2:
            products = Women.objects.all()
        elif product_category == 3:
            products = Boys.objects.all()
        elif product_category == 4:
            products = Girls.objects.all()
        else:
            return redirect('store:error')
        return render(request, 'store/product_list.html', {"products": products})
    except:
        return redirect('store:error')


def collection(request, product_category, product_type):
    """
    Renders a list of products based on the given product category and type.

    Args:
        request (HttpRequest): The HTTP request object.
        product_category (str): The product category code ('M' for Men, 'W' for Women).
        product_type (str): The product type.

    Returns:
        HttpResponse: Rendered product list template or redirects to the error page if invalid category.
    """
    if product_category == 'M':
        products = Men.objects.filter(product_type=product_type)
    elif product_category == 'W':
        products = Women.objects.filter(product_type=product_type)
    else:
        return redirect('store:error')
    return render(request, 'store/product_list.html', {"products": products})


def product_detail(request, product_category, product_pk):
    """
    Renders the details page of a specific product.

    Args:
        request (HttpRequest): The HTTP request object.
        product_category (str): The product category code ('M' for Men, 'W' for Women, 'B' for Boys, 'G' for Girls).
        product_pk (int): The primary key of the product.

    Returns:
        HttpResponse: Rendered product detail page template or redirects to the error page if invalid category.
    """
    try:
        product_model = None
        if product_category == 'M':
            product_model = Men
        elif product_category == 'W':
            product_model = Women
        elif product_category == 'B':
            product_model = Boys
        elif product_category == 'G':
            product_model = Girls
        else:
            return redirect('store:error')

        product = get_object_or_404(product_model, pk=product_pk)
        comments = Reviews.objects.filter(content_type=ContentType.objects.get_for_model(
            product_model), object_id=product_pk)

        if request.method == 'POST' and request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.content_type = ContentType.objects.get_for_model(product_model)
                comment.object_id = product_pk
                comment.save()
                return redirect(f'/product_detail/{product_category}/{product_pk}')
        else:
            form = CommentForm()
        return render(request, 'store/product-page.html', {
            'product': product,
            'comments': comments,
            'form': form,
        })
    except:
        return redirect('store:error')


def error(request):
    """
    Renders the error page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered error page template.
    """
    return render(request, 'error.html')
