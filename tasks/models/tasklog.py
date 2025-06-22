from django.db import models
from users.models.user import User
from projects.models.project import Project

class TaskLog(models.Model):
    id = models.AutoField(primary_key=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id', related_name='task_logs')
    task_number = models.IntegerField()  

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='user_email')

    type = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'task_logs'
        # optional: unique_together = (('project', 'task_number', 'timestamp'),)

    def __str__(self):
        return f"{self.timestamp} | {self.type}"
