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

        user = User.objects(email=email).first()
        if not user:
            return Response({"error": "존재하지 않는 사용자입니다."}, status=404)

        if not check_password(password, user.password):
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=401)

        user.lastLogin = datetime.utcnow()
        user.save()

        token = generate_jwt({
            "user_id": str(user.id),
            "email": user.email,
            "role": user.role
        })

        return Response({
            "message": "로그인 성공",
            "token": token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "role": user.role
            }
        }, status=200)
