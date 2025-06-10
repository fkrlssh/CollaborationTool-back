# tasks/models/tasklog.py
from django.db import models
from .task import Task
from users.models.user import User

class TaskLog(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='task_number')
    project = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='project_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='user_email')
    type = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'task_logs'

    def __str__(self):
        return f"{self.timestamp} | {self.type}"
