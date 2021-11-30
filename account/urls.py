from django.urls import path
from . import views

# Template Tagging
app_name = "account"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
