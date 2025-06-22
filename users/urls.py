from django.urls import path, include
from users.views.register_view import RegisterView, EmailCheckView
from users.views.login_view import LoginView
from users.views.me_view import MeView
from users.views.google_login_view import GoogleLoginView
from users.views.otp_view import send_otp  

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("google-login/", GoogleLoginView.as_view()),
    path("emailcheck/", EmailCheckView.as_view()),
    path("signup/", RegisterView.as_view()),
    path("email/", send_otp), 
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("api/projects/", include("projects.urls")),
    path("api/", include("tasks.urls")),
]
