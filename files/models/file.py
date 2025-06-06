# files/models/file.py
from django.db import models
from users.models.user import User

class File(models.Model):
    project_id = models.IntegerField()
    task_number = models.IntegerField()
    file_number = models.IntegerField()

    uploader = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uploader_email')
    file_name = models.CharField(max_length=255)
    file_url = models.TextField()
    file_type = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField()

    class Meta:
        db_table = 'files'
        unique_together = ('project_id', 'task_number', 'file_number')
