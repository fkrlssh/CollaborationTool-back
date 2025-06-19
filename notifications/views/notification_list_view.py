# notifications/views/notification_list_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.models.notification import Notification

class NotificationListView(APIView):
    def get(self, request):
        user = request.user
        only_unread = request.query_params.get('unread', 'false').lower() == 'true'

        # ✅ 알림 필터링
        notifications = Notification.objects.filter(user=user)
        if only_unread:
            notifications = notifications.filter(is_read=False)

        # ✅ 최신순 정렬
        notifications = notifications.order_by('-created_at')

        data = [
            {
                "id": n.id,
                "type": n.type,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at
            }
            for n in notifications
        ]

        return Response(data, status=status.HTTP_200_OK)
