from django.urls import path
from . import views

# Template Tagging
app_name = "store"

urlpatterns = [
    path("", views.store, name="store"),
    path("category/<slug:slug_value>/", views.store, name="products-by-category"),
    # slug is the name of the view(shoes,pants etc.). Here slug is the attribute of the Category model
    # slug_value is the name of the variable which is passed to the view with the value of slug(shoes,pants etc.). slug_value(you can use any name but you must use the same name in the view)
    path("category/<slug:slug_value>/<slug:product_slug>",
         views.product_detail, name="product-detail"),
    path("search/", views.search, name="search"),
]

# If I do not add 'category' in category/<slug:slug_value>/ and category/<slug:slug_value>/<slug:product_slug> then search/ will not work.

# Because the search route will become like http://127.0.0.1:8000/store/search/.
# We set category route as http://127.0.0.1:8000/store/<category_name>/
# category_name(jeans, shirts etc.)

# Basically it'll look for a category named search and it doesn't exist that's why it throws an error.
