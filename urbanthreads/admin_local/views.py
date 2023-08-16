from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from accounts.models import Order
from django.db.models import Q
from store.models import *
# Create your views here.

PRODUCT_TYPE = (
    ('PANTS', 'PANTS'),
    ('SHORTS', 'SHORTS'),
    ('TSHIRTS', 'T-SHIRTS'),
    ('SHIRTS', 'SHIRTS'),
    ('TROUSERS', 'TROUSERS'),
    ('SHOES', 'SHOES'),
)
"""
A tuple containing choices for product types with their display names.

Each element in the tuple is a two-tuple consisting of the product type code and its display name.
"""

order_count = Order.objects.all().count()
"""
An integer representing the total count of all orders in the system.
"""

PRODUCT_TYPE = ['PANTS', 'SHORTS', 'TSHIRTS', 'SHIRTS', 'TROUSERS', 'SHOES']
"""
A list containing product type codes as strings.

Each element in the list represents a valid product type code that can be used for filtering products.
"""

def admin_local_portal(request):
    """
    Renders the admin portal view for local administrators.

    This view provides details about pending orders, updated orders, and product type counts for men and women categories.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered admin_local.html template with context data.
    """
    orders = Order.objects.filter(order_status='pending')
    orders_updated = Order.objects.filter(Q(order_status='canceled') | Q(order_status='dispatched') | Q(order_status='received'))
    men_type_counts = {}
    women_type_counts = {}
    boys_count = Boys.objects.all().count()
    girls_count = Girls.objects.all().count()
    for product_type in PRODUCT_TYPE:
        men_type_counts[product_type] = Men.objects.filter(product_type=product_type).count()
        women_type_counts[product_type] = Women.objects.filter(product_type=product_type).count()
    return render(request, 'admin_local/admin_local.html', {
        'men_type_counts': men_type_counts,
        'women_type_counts': women_type_counts,
        'girls_count': girls_count,
        'boys_count': boys_count,
        'orders': orders,
        'order_count': order_count,
        'orders_updated': orders_updated,
    })


def order_detail(request, order_pk):
    """
    Renders the order detail view for the specified order.

    This view allows authorized staff to update the order status.

    Args:
        request (HttpRequest): The HTTP request object.
        order_pk (int): The primary key of the order to display.

    Returns:
        HttpResponse: Rendered order-detail.html template with context data.
    """
    is_staff = False
    if request.user.is_authenticated and request.user.is_staff:
        is_staff = True
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.order_status = new_status
        order.save()
        return redirect(f'/order_detail/{order_pk}')
    return render(request, 'admin_local/order-detail.html', {
        'order': order,
        'is_staff': is_staff,
    })
