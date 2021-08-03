from django.db import models
from django.contrib.auth.models import AbstractUser

#继承AbstractUser，增加了余额和电话
class User(AbstractUser):
    phone = models.CharField(max_length=64)
    money = models.FloatField(default=100)
# Create your models here.
