from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


def cart_item(request, get_or_set_session_id, total, quantity, cart_items):
    try:
        tax = 0
        grand_total = 0
        # if user is logged in then cart_items will be if block else it will be else block
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=get_or_set_session_id(request))
            # get all the cart items which has same cart id and is active.
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:    # calculate total price and quantity of the cart items
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (total * 2) / 100  # calculate the 2% tax
        grand_total = total + tax   # calculate the grand total after tax

    except ObjectDoesNotExist:
        pass    # do nothing
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return context
