# projects/models/projectmember.py
from django.db import models
from users.models.user import User
from .project import Project

class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('guest', 'Guest'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_email')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'project_members'
        unique_together = ('project', 'user')
