from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('internship.urls')), 
     path('api/', include('internship.urls')),
]
