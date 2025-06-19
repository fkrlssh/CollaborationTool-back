# notifications/services/create_notification.py
from notifications.models.notification import Notification
from django.utils import timezone

def create_notification(user, type, message):
    Notification.objects.create(
        user=user,
        type=type,
        message=message,
        is_read=False,
        created_at=timezone.now()
    )
