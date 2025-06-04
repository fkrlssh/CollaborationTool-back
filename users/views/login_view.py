from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models.user import User
from utils.hash import check_password
from utils.jwt_token import generate_jwt
from datetime import datetime

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "이메일과 비밀번호를 입력하세요."}, status=400)

        user = User.objects.filter(email=email).first()
        if not user or not check_password(password, user.password):
            return Response({"error": "이메일 또는 비밀번호가 잘못되었습니다."}, status=401)

        user.lastLogin = datetime.now()
        user.save()

        token = generate_jwt({
            "email": user.email
        })

        return Response({
            "success": True,
            "token": token,
            "user": {
                "email": user.email,
                "name": user.name,
                "lastLogin": user.last_login
            }
        }, status=200)
