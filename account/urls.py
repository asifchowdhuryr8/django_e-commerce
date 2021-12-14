from django.urls import path
from . import views

# Template Tagging
app_name = "account"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("activate_account/<uidb64>/<token>/",
         views.activate_account, name="activate_account"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
