from django.contrib import admin
from django.urls import path, include
from . import views
from django.http import JsonResponse

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/test/", views.test_api),  
    path("api/", include("users.urls")),
    path('projects/', include('projects.urls')),

    path('health/', lambda request: JsonResponse({'status': 'OK'})),
]
