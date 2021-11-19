from django.shortcuts import get_object_or_404, render
from .models import Product
from category.models import Category

# Create your views here.


def store(request, slug_value=None):
    categories = None
    products = None
    if slug_value:
        # get_object_or_404 #If it finds anything then it'll render them otherwise render 404 page
        categories = get_object_or_404(Category, slug=slug_value)
        products = Product.objects.filter(
            category=categories, is_available=True)
        total_product = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        total_product = products.count()

    context = {'products': products, 'total_product': total_product}
    return render(request, 'store/store.html', context)
