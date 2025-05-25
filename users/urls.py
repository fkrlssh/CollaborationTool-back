from django.urls import path
from users.views.auth_view import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),
]
