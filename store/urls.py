from django.urls import path
from . import views

# Template Tagging
app_name = "store"

urlpatterns = [
    path("", views.store, name="store"),
]
