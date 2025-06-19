# users/views/me_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.auth import jwt_required
from users.models.user import User

class MeView(APIView):
    @jwt_required
    def get(self, request):
        user = request.user

        if not user or not isinstance(user, User):
            return Response(
                {"error": "인증된 사용자 정보를 불러올 수 없습니다."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            "id": user.email,
            "email": user.email,
            "name": user.name,
            "lastLogin": user.last_login,
            "authProvider": user.auth_provider
        }, status=status.HTTP_200_OK)
