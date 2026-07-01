from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Template views
    path('', include('apps.destinos.urls')),
    path('', include('apps.usuarios.urls')),
    path('grupos/', include('apps.grupos.urls')),
    path('feed/', include('apps.feed.urls')),

    # REST API
    path('api/', include([
        path('auth/', include('apps.usuarios.api_urls')),
        path('destinos/', include('apps.destinos.api_urls')),
        path('comentarios/', include('apps.comentarios.api_urls')),
        path('grupos/', include('apps.grupos.api_urls')),
        path('feed/', include('apps.feed.api_urls')),
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
