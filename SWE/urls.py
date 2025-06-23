from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from users.views.custom_token_view import CustomTokenObtainPairView
from projects.views.create_project_view import ProjectCreateApiView
from projects.views.project_list_view import ProjectListView
from users.views.otp_view import send_otp

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/test/", lambda request: JsonResponse({'status': 'OK'})),
    path("api/", include("users.urls")),  
    path("projects/", include("projects.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/project/", ProjectCreateApiView.as_view(), name="project-api-create"),
    path("api/getprojects/", ProjectListView.as_view()),
    path("api/projects/", include("projects.urls")),
    path("api/", include("tasks.urls")),
    path('api/', include('comments.urls')),

]
