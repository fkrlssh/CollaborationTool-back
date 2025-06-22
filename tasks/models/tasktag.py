from django.db import models
from projects.models.project import Project

class TaskTag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id', related_name='task_tags')
    task_number = models.IntegerField()
    tag = models.CharField(max_length=50)

    class Meta:
        db_table = 'task_tags'
        unique_together = ('project', 'task_number', 'tag')

    def __str__(self):
        return f"{self.project.id} - {self.task_number} - {self.tag}"
