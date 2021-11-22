from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import get_or_set_session_id
from django.core.paginator import Paginator
# Create your views here.


def store(request, slug_value=None):
    products = None
    if slug_value:
        # get_object_or_404 #If it finds anything then it'll render them otherwise render 404 page
        categories = get_object_or_404(Category, slug=slug_value)
        products = Product.objects.filter(
            category=categories, is_available=True)
        total_product = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        # get the page variable value from the url
        products = paginator.get_page(page)
        # now products variable is a paginator object. It has all the products in it which is coming from filter method But will render accordingly paginator.
    else:
        products = Product.objects.all().filter(is_available=True)
        total_product = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        products = paginator.get_page(page)

    context = {'products': products, 'total_product': total_product}
    return render(request, 'store/store.html', context)


def product_detail(request, slug_value, product_slug):
    try:
        product = Product.objects.get(
            slug=product_slug, is_available=True)
        in_cart = CartItem.objects.filter(
            cart__cart_id=get_or_set_session_id(request), product=product).exists()
    except Exception as e:
        raise e
    context = {'product': product, 'in_cart': in_cart}
    return render(request, 'store/product-detail.html', context)
