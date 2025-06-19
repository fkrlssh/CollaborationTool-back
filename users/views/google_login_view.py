from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from users.models.user import User
from utils.jwt_token import generate_jwt
from datetime import datetime
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("id_token")
        if not token:
            return Response({"error": "id_token이 필요합니다."}, status=400)

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            email = idinfo["email"]
            name = idinfo.get("name", "이름 없음")

            user = User.objects.filter(email=email).first()

            if not user:
                user = User.objects.create(
                    email=email,
                    name=name,
                    auth_provider="google"
                )
            elif user.auth_provider != "google":
                return Response({
                    "error": "해당 이메일은 일반 로그인 방식으로 이미 등록되어 있습니다."
                }, status=409)

            user.last_login = datetime.utcnow()
            user.save()

            jwt_token = generate_jwt({"email": user.email})

            return Response({
                "success": True,
                "token": jwt_token,
                "user": {
                    "email": user.email,
                    "name": user.name
                }
            })

        except ValueError:
            return Response({"error": "유효하지 않은 Google 토큰입니다."}, status=401)
