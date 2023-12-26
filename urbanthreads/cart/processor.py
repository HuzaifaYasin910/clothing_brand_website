from accounts.models import Cart
from store.models import Clothing



def get_cart_data(request):
    cart_products = []
    total_price = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_products = cart.cart_products.all()
            total_price = sum(product.product.product_price * product.quantity for product in cart_products)
            guest = False
    else:
        cart = request.session.get('cart', {})
        product_ids = cart.keys()
        cart_products = Clothing.objects.filter(pk__in=product_ids)
        total_price = sum(product.product_price * cart[str(product.pk)] for product in cart_products)
        guest=True
    print(cart)
    return {'cart_products': cart_products, 'total_price': total_price,'guest':guest}