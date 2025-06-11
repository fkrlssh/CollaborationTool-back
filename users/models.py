from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password, name):
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    email    = models.EmailField(primary_key=True, max_length=254)
    name     = models.CharField(max_length=100)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
