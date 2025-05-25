from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models.user import User
from utils.hash import hash_password
from mongoengine.errors import NotUniqueError

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if not email or not password or not name:
            return Response({"error": "모든 항목을 입력하세요."}, status=400)

        hashed_pw = hash_password(password)

        try:
            user = User(
                email=email,
                password=hashed_pw,
                name=name,
                role="user"
            ).save()
        except NotUniqueError:
            return Response({"error": "이미 존재하는 이메일입니다."}, status=409)

        return Response({
            "message": "회원가입 성공",
            "user_id": str(user.id)
        }, status=status.HTTP_201_CREATED)
