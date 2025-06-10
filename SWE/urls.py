from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/test/", views.test_api),  
    path("api/", include("users.urls")),

]
