# utils/auth.py
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from utils.jwt_token import decode_jwt
from users.models.user import User



def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"error": "인증 정보가 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        payload = decode_jwt(token)
        if not payload:
            return Response({"error": "유효하지 않거나 만료된 토큰입니다."}, status=status.HTTP_401_UNAUTHORIZED)

        user_email = payload.get("email")
        user = User.objects.filter(email=user_email).first()

        if not payload:
            return Response({"error": "유효하지 않거나 만료된 토큰입니다."}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(email=payload.get("email")).first()
        if not user:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        request.user = user  # 사용자 객체를 request에 주입
        return view_func(self, request, *args, **kwargs)

    return _wrapped_view
