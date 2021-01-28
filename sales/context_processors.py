from sales.models.order import ShopCart
from sales.views.cart import Cart
from sales.views.views import shopcart


def cart(request):
    current_user = request.user  # Access User Session information
    return {'cart': Cart(request),'shopcart':ShopCart.objects.filter(user_id=current_user.id)}