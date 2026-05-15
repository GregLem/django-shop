from .views import get_or_create_cart

def cart_items_count(request):
    cart = get_or_create_cart(request)
    count = sum(item.quantity for item in cart.items.all())
    return {'cart_items_count': count}