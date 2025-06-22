# users/views/otp_view.py

import random
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import EmailOTP  # models/__init__.py에 등록돼 있어야 함
from rest_framework import status



def generate_otp():
    return f"{random.randint(100000, 999999)}"

@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': '이메일을 입력해주세요.'}, status=400)

    otp = generate_otp()
    now = timezone.now()
    expires_at = now + timezone.timedelta(minutes=5)

    # 기존 기록이 있으면 덮어쓰기
    EmailOTP.objects.update_or_create(
        email=email,
        defaults={'otp_code': otp, 'created_at': now, 'expires_at': expires_at}
    )

    # 이메일 발송
    try:
        send_mail(
            subject='회원가입 인증 코드',
            message=f'인증 번호는 {otp} 입니다. 5분 내에 입력해주세요.',
            from_email=settings.EMAIL_HOST_USER,  # settings.py에서 설정한 발신 주소
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({'error': f'이메일 발송 실패: {str(e)}'}, status=500)

    return Response({'message': 'OTP가 이메일로 전송되었습니다.'})
