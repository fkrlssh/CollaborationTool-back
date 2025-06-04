from django.urls import path
from users.views.register_view import RegisterView
from users.views.login_view import LoginView
from users.views.me_view import MeView
from users.views.google_login_view import GoogleLoginView
from users.views.register_view import RegisterView, EmailCheckView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("google-login/", GoogleLoginView.as_view()),
    path("api/signup",RegisterView.as_view()),
    path("emailcheck/", EmailCheckView.as_view()),
    path("signup", RegisterView.as_view()),
    ]  
