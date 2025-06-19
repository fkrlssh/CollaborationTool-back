# notifications/views/notification_read_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.models.notification import Notification

class NotificationReadView(APIView):
    def post(self, request, notification_id):
        user = request.user

        try:
            notification = Notification.objects.get(id=notification_id, user=user)
        except Notification.DoesNotExist:
            return Response({'error': '해당 알림을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if notification.is_read:
            return Response({'message': '이미 읽은 알림입니다.'}, status=status.HTTP_200_OK)

        notification.is_read = True
        notification.save()

        return Response({'message': '알림이 읽음 처리되었습니다.'}, status=status.HTTP_200_OK)
