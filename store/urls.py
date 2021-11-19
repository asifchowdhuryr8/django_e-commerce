from django.urls import path
from . import views

# Template Tagging
app_name = "store"

urlpatterns = [
    path("", views.store, name="store"),
    path("<slug:slug_value>/", views.store, name="products_by_category"),
    # slug is the name of the view(shoes,pants etc.). Here slug is the attribute of the Category model
    # slug_value is the name of the variable which is passed to the view with the value of slug(shoes,pants etc.). slug_value(you can use any name but you must use the same name in the view)
]
