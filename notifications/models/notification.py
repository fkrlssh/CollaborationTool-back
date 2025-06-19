from django.db import models
from users.models.user import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_email')
    type = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'notifications'
