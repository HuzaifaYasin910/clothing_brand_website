from accounts.models import CartProduct
import json
from django.http import HttpResponse,JsonResponse





# for users , add fresh data to cookie cart
def user_cookies(request):
    user_cart_products = CartProduct.objects.filter(user=request.user)
    cart_data = {}
    for cart_product in user_cart_products:
        item_data= {
        'product':str(cart_product.product.uid),
        'quantity':cart_product.quantity,
        'color':cart_product.color,
        'size':cart_product.size
        }
        cart_data[cart_product.pk] = item_data
    return JSONENCODE(cart_data)

# for guests ,will create if not exist , will +1 if exist
def guest_cookies(request):
    cookie_cart = request.COOKIES.get('cart')
    index = request.POST.get('product_id')
    color = request.POST.get('color')
    size  = request.POST.get('size')
    quantity = request.POST.get('quantity')
    product = request.POST.get('product_id')
    index = index+size+color
    if cookie_cart:
        cookie_cart = JSONDECODE(cookie_cart)
        if cookie_cart.get(index) is not None:
            if cookie_cart[index]['quantity'] < 5:
                cookie_cart[index]['quantity'] += 1
                return JSONENCODE(cookie_cart)
            return JSONENCODE(cookie_cart)
        else:
            cookie_cart[index]={
            'product':product,
            'quantity':1,
            'color':color,
            'size':size,
            }
        return JSONENCODE(cookie_cart)
    else:
        cookie_cart = {}
        cookie_cart[index]={
            'product':product,
            'quantity':1,
            'color':color,
            'size':size,
            }
        return JSONENCODE(cookie_cart)
        

def JSONDECODE(json_data):
    try:return json.loads(json_data)
    except Exception as e:return HttpResponse('error in handeling of json data',e)

def JSONENCODE(json_data):
    try:return json.dumps(json_data)
    except Exception as e:return HttpResponse('error in handeling of json data',e)