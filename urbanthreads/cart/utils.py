from accounts.models import CartProduct
import json
from django.http import HttpResponse

def helper_cookies(user):
    user_cart_products = CartProduct.objects.filter(user=user)
    cart_data = {}
    for item in user_cart_products:
        item_data= {
        'quantity': item.quantity,
        'color':item.color,
        'size': item.size,
        }
        cart_data[str(item.product.uid)] = item_data
    return json.dumps(cart_data)

def make_cookies(request):
    user_cart_products = CartProduct.objects.filter(user=request.user)
    cart_data = {}
    for item in user_cart_products:
        item_data= {
        'quantity': item.quantity,
        'color':item.color,
        'size': item.size,
        }
        cart_data[str(item.product.uid)] = item_data
    return json.dumps(cart_data)

def set_guest_cart_cookie(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        res = request.COOKIES.get('cart')
        if res is not None:
            try:res = json.loads(res)
            except:return 
            if res.get(product_id) is not None:
                if res[product_id]['quantity'] < 5:
                    res[product_id]['quantity'] += 1
                    return json.dumps(res) 
                return json.dumps(res) 
            else:
                res[product_id]={
                'quantity': 1,
                'color': request.POST.get('color'),
                'size': request.POST.get('size')
                }
                return json.dumps(res)
        else:
            res = {}
            res[product_id]={
            'quantity': 1,
            'color': request.POST.get('color'),
            'size': request.POST.get('size')
            }
            return json.dumps(res)

def JSONDECODE(json_data):
    try:return json.loads(json_data)
    except Exception as e:return HttpResponse('error in handeling of json data',e)
def JSONENCODE(json_data):
    try:return json.dumps(json_data)
    except Exception as e:return HttpResponse('error in handeling of json data',e)