from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    age = models.IntegerField()
    balance = models.FloatField()
    bonus = models.FloatField()

    def __str__(self) -> str:
        return self.user.username
