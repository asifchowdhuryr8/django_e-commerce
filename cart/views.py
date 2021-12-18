from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from .utils import cart_item


def get_or_set_session_id(request):
    """If user is log in the get his session id otherwise create a session id for guest user"""
    # session_id(whenever a user log in with there credentials then a temporary session_id is created inside the browser[django's default authentication system]) and it is stored in the browser's local storage. If the user logs out then the session_id is deleted from the browser's local storage.
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):

    product = Product.objects.get(id=product_id)    # get the product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:   # Loop through the request.POST
            key = item  # get the key.
            value = request.POST[key]   # get the value.
            # If ?color=red&size=M then key will be color and value will be red. second time key will be size and value will be M and so on. If there are any other query string parameters then they will be added to like csrf token.

            try:
                variation = Variation.objects.get(
                    product=product, variation__iexact=key, variation_value__iexact=value)
                # Making sure that variation get the exact product which has this exact key and value.
                product_variation.append(variation)
                print(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=get_or_set_session_id(
            request))  # get the cart if there is any
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=get_or_set_session_id(request))   # create a new cart with the session id as cart id
        cart.save()   # save the cart to the database

    is_cart_item_exist = CartItem.objects.filter(
        product=product, cart=cart).exists()
    if is_cart_item_exist:
        # get the cart item if the product is already in the cart
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        existing_variation_item_list = []
        existing_variation_item_id = []
        for item in cart_item:
            """get all the variations of the cart item and their ids"""
            existing_variation_item = item.variation.all()
            existing_variation_item_list.append(list(existing_variation_item))
            existing_variation_item_id.append(item.id)

        if product_variation in existing_variation_item_list:
            """If a user has already bought a product of this same category then update the quantity. e.g. user bought a shirt (blue+40) then if he want to buy another then update the quantity from the previous cart item"""
            index = existing_variation_item_list.index(
                product_variation)   # get the index of the number
            # get the id of the cart item
            item_id = existing_variation_item_id[index]
            cart_item = CartItem.objects.get(
                product=product, id=item_id)   # get the cart item
            cart_item.quantity += 1
            cart_item.save()
    else:
        #     """If a user buy a new product or buy the same product with another category then add it as a new cart item. e.g. user adds  a shirt (blue+40) to his cart and again adds a new shirt (black+30) to his cart. In this case add two item in the cart"""
        cart_item = CartItem.objects.create(
            product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variation.clear()   # clear the previously selected variations
            # add all the product variations
            cart_item.variation.add(*product_variation)
        cart_item.save()
    return redirect('cart:cart')    # redirect to the cart page


def decrease_cart_item_quantity(request, product_id, cart_item_id):
    cart = Cart.objects.get(
        cart_id=get_or_set_session_id(request))  # get the cart
    # get the product and if it doesn't exist return 404 error
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)    # get the cart item
        if cart_item.quantity > 1:  # if the quantity is greater than 1 then decrement the quantity
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # if the quantity is 1 then delete the cart item
    except ObjectDoesNotExist:
        pass
    return redirect('cart:cart')    # redirect to the cart page


def remove_cart_item(request, product_id, cart_item_id):
    """Delete the cart item if user clicks the delete button from cart page"""
    cart = Cart.objects.get(cart_id=get_or_set_session_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except ObjectDoesNotExist:
        pass
    return redirect('cart:cart')


def cart(request, total=0, quantity=0, cart_items=None):
    context = cart_item(request, get_or_set_session_id,
                        total, quantity, cart_items)
    return render(request, 'cart/cart.html', context)


def checkout(request, total=0, quantity=0, cart_items=None):
    context = cart_item(request, get_or_set_session_id,
                        total, quantity, cart_items)
    return render(request, 'cart/checkout.html', context)
