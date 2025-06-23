# tasks/models/tasklog.py

from django.db import models
from users.models.user import User
from tasks.models.task import Task  

class TaskLog(models.Model):
    id = models.AutoField(primary_key=True)

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='logs')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='user_email')

    type = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'task_logs'

    def __str__(self):
        return f"{self.timestamp} | {self.task.task_number} | {self.type}"
