from django.urls import path
from . import views

# Template Tagging
app_name = "category"

urlpatterns = [
    path("", views.homepage, name="homepage"),
]

