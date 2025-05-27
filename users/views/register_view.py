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
            return Response({
                "success": False,
                "error": "모든 항목을 입력해주세요."
            }, status=status.HTTP_400_BAD_REQUEST)

        hashed_pw = hash_password(password)

        try:
            user = User(
                email=email,
                password=hashed_pw,
                name=name
            ).save()
        except NotUniqueError:
            return Response({
                "success": False,
                "error": "이미 등록된 이메일입니다."
            }, status=status.HTTP_409_CONFLICT)

        return Response({
            "success": True,
            "user": {
                "email": user.email,
                "name": user.name,
                "createdAt": user.createdAt
            }
        }, status=status.HTTP_201_CREATED)
