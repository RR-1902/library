from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("secure-admin/", admin.site.urls),
    path("", include("store.urls")),
]
