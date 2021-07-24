from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=64)
    #token = models.CharField(max_length=255)
    money = models.FloatField(default=100)
# Create your models here.
