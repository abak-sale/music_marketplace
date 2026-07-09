from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Menambahkan sistem login & logout bawaan Django di sini
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', include('homepage.urls')),
    path('products/', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)