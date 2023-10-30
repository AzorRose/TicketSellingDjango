from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")


    first_name = models.CharField(max_length=32, null=True)
    second_name = models.CharField(max_length=32, null=True)
    
    genders = [
        ("F", "Female"),
        ("M", "Male"),
        ("undefined", "undefined"),
    ]
    
    gender = models.CharField(max_length=9, choices=genders, default="undefined")
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    age = models.IntegerField()
    balance = models.FloatField()
    bonus = models.FloatField()

    def __str__(self) -> str:
        return self.user.username
