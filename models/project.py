# projects/models/project.py
from django.db import models
from users.models.user import User

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner_email = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner_email')
    created_at = models.DateTimeField()
    access = models.BooleanField(default=False)  # TINYINT → Boolean으로 매핑

    class Meta:
        db_table = 'projects'
