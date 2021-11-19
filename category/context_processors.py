from .models import Category


def category_list(request):
    """Get all the category item from the database and convert them to a dictionary as well as return the dictionary"""
    categories = Category.objects.all()
    return dict(categories=categories)
