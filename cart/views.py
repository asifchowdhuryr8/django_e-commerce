from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem


def get_or_set_session_id(request):
    """If user is log in the get his session id otherwise create a session id for guest user"""
    # session_id(whenever a user log in with there credentials then a temporary session_id is created inside the browser[django's default authentication system]) and it is stored in the browser's local storage. If the user logs out then the session_id is deleted from the browser's local storage.
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)    # get the product

    try:
        cart = Cart.objects.get(cart_id=get_or_set_session_id(
            request))  # get the cart if there is any
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=get_or_set_session_id(request))   # create a new cart with the session id as cart id
        cart.save()   # save the cart to the database

    try:
        # get the cart item if the product is already in the cart
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # update the product quantity of the cart item
        cart_item.save()    # save the cart item to the database

    except CartItem.DoesNotExist:   # if the product is not in the cart create a new cart item with the product and set quantity 1 as well as save it to the database
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart')    # redirect to the cart page


def decrease_cart_item_quantity(request, product_id):
    cart = Cart.objects.get(
        cart_id=get_or_set_session_id(request))  # get the cart
    # get the product and if it doesn't exist return 404 error
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(
        product=product, cart=cart)    # get the cart item
    if cart_item.quantity > 1:  # if the quantity is greater than 1 then decrement the quantity
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # if the quantity is 1 then delete the cart item
    return redirect('cart:cart')    # redirect to the cart page


def remove_cart_item(request, product_id):
    """Delete the cart item if user clicks the delete button from cart page"""
    cart = Cart.objects.get(cart_id=get_or_set_session_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
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
    return render(request, 'cart/cart.html', context)
