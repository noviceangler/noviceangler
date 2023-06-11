from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from noviceAngler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('noviceAngler/', include('noviceAngler.urls')),
    path('common/', include('common.urls')),
]
urlpatterns += static (
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)