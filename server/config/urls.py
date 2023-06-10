from django.contrib import admin
from django.urls import path, include
from noviceAngler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('noviceAngler/', include('noviceAngler.urls')),
    path('common/', include('common.urls')),
    path('', views.index, name='index'),
]
