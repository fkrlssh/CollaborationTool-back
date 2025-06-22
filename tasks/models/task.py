# tasks/models/task.py
from django.db import models
from projects.models.project import Project
from users.models.user import User

class Task(models.Model):
    id = None  

    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id', primary_key=True)
    task_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='assignee_email')
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')],
        default='To Do'
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'tasks'
        unique_together = ('project', 'task_number')
        managed = False

    def __str__(self):
        return f"[{self.project.id}] {self.task_number} - {self.title}"
