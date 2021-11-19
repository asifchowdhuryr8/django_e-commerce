from django.shortcuts import render
from .models import Product

# Create your views here.


def store(request):
    products = Product.objects.all().filter(is_available=True)
    total_product = products.count()
    context = {'products': products, 'total_product': total_product}
    return render(request, 'store/store.html', context)
