from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import mimetypes
from django.contrib.auth import views as auth_views


mimetypes.add_type("text/javascript", ".mjs")

urlpatterns = [
    path('', include('files.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path("admin/logout/", auth_views.LogoutView.as_view(), name="logout"),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
