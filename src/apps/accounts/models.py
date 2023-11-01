from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


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

    class Meta:
        db_table = "Users"

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, age=0, balance=0, bonus=0)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
