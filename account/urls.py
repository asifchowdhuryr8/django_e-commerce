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
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("validate_reset_password_link/<uidb64>/<token>/",
         views.validate_reset_password_link, name="validate_reset_password_link"),
    path("reset_password/", views.reset_password, name="reset_password"),
]
