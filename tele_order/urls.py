from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('super-secret-admin/', admin.site.urls),
]
