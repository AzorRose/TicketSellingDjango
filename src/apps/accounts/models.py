from typing import Any
from django.db import models
from django.contrib.auth.models import User
from apps.events.models import Ticket
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name="profile"
    )

    first_name = models.CharField(max_length=32, null=True)
    second_name = models.CharField(max_length=32, null=True)
    gender = models.CharField(max_length=9)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    age = models.IntegerField()
    balance = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    buyback_sum = models.FloatField(default=0)

    bonus_levels = {5000: 0, 10000: 2, 30000: 5, 10000000: 10}

    def count_buyback(self):
        purchases = Purchase.objects.filter(user=self)
        summary = 0
        for i in purchases:
            summary += i.ticket.price
        self.buyback_sum = summary
        self.save(update_fields=["buyback_sum"])
        self.count_bonus()
        self.count_age()

    def count_bonus(self):
        for i in self.bonus_levels:
            if self.buyback_sum < i:
                self.bonus = self.bonus_levels[i]
                break
        self.save(update_fields=["bonus"])

    def count_age(self):
        today = date.today()
        self.age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        self.save(update_fields=["age"])

    def __str__(self) -> str:
        return self.user.username
            
    class Meta:
        db_table = "Users"
        
    def get_default_user():
        return UserProfile.objects.get(user=User.objects.get(username="empty"))


class Purchase(models.Model):
    
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_DEFAULT, related_name="purchase", default=UserProfile.get_default_user)

    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING, related_name="+")

    def save(self, *args, **kwargs):
        super(Purchase, self).save(*args, **kwargs)
        self.user.count_buyback()
