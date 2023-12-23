# from django.http import HttpResponse
# from django.shortcuts import render,get_object_or_404,redirect
# from accounts.models import Order
# from django.db.models import Q
# from store.models import *
# from .forms import ClothingForm
# # Create your views here.

# PRODUCT_TYPE = (
#     ('PANTS', 'PANTS'),
#     ('SHORTS', 'SHORTS'),
#     ('TSHIRTS', 'T-SHIRTS'),
#     ('SHIRTS', 'SHIRTS'),
#     ('TROUSERS', 'TROUSERS'),
#     ('SHOES', 'SHOES'),
# )
# """
# A tuple containing choices for product types with their display names.

# Each element in the tuple is a two-tuple consisting of the product type code and its display name.
# """

# order_count = Order.objects.all().count()
# """
# An integer representing the total count of all orders in the system.
# """

# PRODUCT_TYPE = ['PANTS', 'SHORTS', 'TSHIRTS', 'SHIRTS', 'TROUSERS', 'SHOES']
# """
# A list containing product type codes as strings.

# Each element in the list represents a valid product type code that can be used for filtering products.
# """

# def order_detail(request, order_pk):
#     """
#     Renders the order detail view for the specified order.

#     This view allows authorized staff to update the order status.

#     Args:
#         request (HttpRequest): The HTTP request object.
#         order_pk (int): The primary key of the order to display.

#     Returns:
#         HttpResponse: Rendered order-detail.html template with context data.
#     """
#     is_staff = False
#     if request.user.is_authenticated and request.user.is_staff:
#         is_staff = True
#     order = get_object_or_404(Order, pk=order_pk)
#     if request.method == 'POST':
#         new_status = request.POST.get('new_status')
#         order.order_status = new_status
#         order.save()
#         return redirect(f'/order_detail/{order_pk}')
#     return render(request, 'admin_local/order-detail.html', {
#         'order': order,
#         'is_staff': is_staff,
#     })

# def clothing_create_view(request):
#     if request.method == 'POST':
#         clothing_form = ClothingForm(request.POST)
#         print(clothing_form)
#         # if all(form.is_valid() for form in [clothing_form, size_formset, colors_formset, images_formset]):
#         #     clothing = clothing_form.save(commit=False)
#         #     clothing.save()

#         #     size_instances = size_formset.save(commit=False)
#         #     for instance in size_instances:
#         #         instance.clothing = clothing
#         #         instance.save()

#         #     colors_instances = colors_formset.save(commit=False)
#         #     for instance in colors_instances:
#         #         instance.clothing = clothing
#         #         instance.save()

#         #     images_instances = images_formset.save(commit=False)
#         #     for instance in images_instances:
#         #         instance.clothing = clothing
#         #         instance.save()

#         #     # Redirect or perform any other action after successful form submission
#         #     return redirect('success_page')
#     else:
#         clothing_form = ClothingForm()

#     return render(request, 'admin_local/input.html', {
#         'clothing_form': clothing_form,
#     })