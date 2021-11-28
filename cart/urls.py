from django.urls import path
from . import views

# Template Tagging
app_name = "cart"

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add_card/<int:product_id>/", views.add_cart, name="add_cart"),
    path("decrease_cart_item_quantity/<int:product_id>/<int:cart_item_id>/",
         views.decrease_cart_item_quantity, name="decrease_cart_item_quantity"),
    path("remove_cart_item/<int:product_id>/<int:cart_item_id>/",
         views.remove_cart_item, name="remove_cart_item"),
]
