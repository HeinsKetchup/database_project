from django.db import models

# Create your models here.
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class InsecureUser(models.Model):
    user_data = models.JSONField()
