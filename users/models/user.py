from django.db import models

class User(models.Model):
    AUTH_CHOICES = (
        ('local', 'Local'),
        ('google', 'Google'),
    )

    email = models.EmailField(primary_key=True)  
    password = models.CharField(max_length=255)  
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def str(self):
        return self.email

    class Meta:
        db_table = 'users'  