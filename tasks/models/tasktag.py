# tasks/models/tasktag.py
from django.db import models
from .task import Task

class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='task_number')
    project = models.ForeignKey(Task, on_delete=models.CASCADE, db_column='project_id')
    tag = models.CharField(max_length=50)

    class Meta:
        db_table = 'task_tags'
        unique_together = ('project', 'task', 'tag')

    def __str__(self):
        return f"{self.project.id} - {self.task.task_number} - {self.tag}"
