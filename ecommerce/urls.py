from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('category.urls')),
    path('admin/', admin.site.urls),
    path('category/', include('category.urls')),
]
