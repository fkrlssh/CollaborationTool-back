# comments/models/comment.py
from django.db import models
from tasks.models.task import Task
from users.models.user import User

class Comment(models.Model):
    id=None
    project_id = models.IntegerField()
    task_number = models.IntegerField()
    comment_number = models.IntegerField(primary_key=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_email')
    content = models.TextField()
    edited = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'comments'
        unique_together = ('project_id', 'task_number', 'comment_number')
