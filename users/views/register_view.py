from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models.user import User
from utils.hash import hash_password
from django.db import IntegrityError
from django.utils import timezone
from django.http import JsonResponse
from users.models import EmailOTP


class EmailCheckView(APIView):
    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({
                "success": False,
                "error": "이메일이 제공되지 않았습니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        exists = User.objects.filter(email=email).exists()

        return Response({
            "success": True,
            "isDuplicate": exists
        }, status=status.HTTP_200_OK)




class RegisterView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        otp = data.get("otp")  #  추가된 필드

        # 기본 필수 입력값 확인
        if not email or not password or not name or not otp:
            return Response({
                "success": False,
                "error": "모든 항목(이메일, 비밀번호, 이름, 인증번호)을 입력해주세요."
            }, status=status.HTTP_400_BAD_REQUEST)

        #  OTP 검증
        try:
            otp_record = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            return Response({
                "success": False,
                "error": "OTP 인증 정보가 존재하지 않습니다. 먼저 인증 코드를 요청해주세요."
            }, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.otp_code != otp:
            return Response({
                "success": False,
                "error": "인증 코드가 올바르지 않습니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        if otp_record.is_expired():
            return Response({
                "success": False,
                "error": "인증 코드가 만료되었습니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        #  비밀번호 해시 및 사용자 생성
        hashed_pw = hash_password(password)

        try:
            user = User.objects.create(
                email=email,
                password=password,
                name=name,
                created_at=timezone.now()
            )
            otp_record.delete()  #  회원가입 완료 시 OTP 삭제
        except IntegrityError:
            return Response({
                "success": False,
                "error": "이미 등록된 이메일입니다."
            }, status=status.HTTP_409_CONFLICT)

        return Response({
            "success": True,
            "user": {
                "email": user.email,
                "name": user.name,
                "createdAt": user.created_at
            }
        }, status=status.HTTP_201_CREATED)
