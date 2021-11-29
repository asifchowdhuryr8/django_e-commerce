from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('category.urls')),
    path('admin/', admin.site.urls),
    path('category/', include('category.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('account/', include('account.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
