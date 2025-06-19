from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models.user import User
from utils.jwt_token import generate_jwt
from django.utils import timezone
from rest_framework.permissions import AllowAny
import logging


logging.basicConfig(
    filename="login_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger(__name__)


class LoginView(APIView):
    permission_classes = [AllowAny]  # 

    def post(self, request):
        logger.warning("LoginView 진입 확인됨")  # 진입 로그

        email = request.data.get("email")
        password = request.data.get("password")

        logger.debug(f"입력 이메일: {email}")
        logger.debug(f"입력 비밀번호: {password}")

        if not email or not password:
            logger.warning("이메일 또는 비밀번호 누락")
            return Response({"error": "이메일과 비밀번호를 입력하세요."}, status=400)

        try:
            user = User.objects.filter(email=email).first()
            logger.debug(f"DB 조회된 유저: {user}")
        except Exception as e:
            logger.error(f"DB 오류: {str(e)}")
            return Response({"error": f"DB 오류: {str(e)}"}, status=500)

        if not user:
            logger.warning(f"사용자 없음: {email}")
        elif not user.check_password(password):
            logger.warning("비밀번호 불일치")
            logger.debug(f"입력된 비밀번호: {password}")
            logger.debug(f"DB 해시: {user.password}")
            logger.debug(f"check_password 결과: {user.check_password(password)}")

        if not user or not user.check_password(password):
            return Response({"error": "이메일 또는 비밀번호가 잘못되었습니다."}, status=401)

        user.last_login = timezone.now()
        user.save()

        token = generate_jwt({
            "email": user.email
        })

        logger.info(f"로그인 성공: {email}")

        return Response({
            "success": True,
            "token": token,
            "user": {
                "email": user.email,
                "name": user.name,
                "lastLogin": user.last_login
            }
        }, status=200)
