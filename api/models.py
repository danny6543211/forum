from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.TextField()

    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=10)