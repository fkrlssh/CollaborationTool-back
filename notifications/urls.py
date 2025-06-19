from django.urls import path
from notifications.views.notification_list_view import NotificationListView
from notifications.views.notification_read_view import NotificationReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>/read/', NotificationReadView.as_view(), name='notification-read'),
]
