from django.contrib import admin
from django.urls import path, include
from . import views
from django.http import JsonResponse

from datetime import timedelta
from users.views.custom_token_view import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/test/", views.test_api),  
    path("api/", include("users.urls")),
    path('projects/', include('projects.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('health/', lambda request: JsonResponse({'status': 'OK'})),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/notifications/", include("notifications.urls"))
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # 기타 옵션...
}