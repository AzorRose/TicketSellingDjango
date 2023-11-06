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
    balance = models.FloatField()
    bonus = models.FloatField()
    buyback_sum = models.FloatField(default=0)

    bonus_levels = {5000: 0, 10000: 2, 30000: 5, float("inf"): 10}

    def buyback_count(self):
        purchases = Purchase.objects.filter(user=self)
        summary = 0
        for i in purchases:
            summary += i.ticket.price
        self.buyback_sum = summary
        self.user.save()
        self.bonus_count()

    def bonus_count(self):
        for i in self.bonus_levels:
            if self.buyback_sum < i:
                self.bonus = self.bonus_levels[i]
                break

        self.user.save()

    def age_count(self):
        today = date.today
        self.age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        self.user.save()
        
    class Meta:
        db_table = "Users"

    def __str__(self) -> str:
        return self.user.username



class Purchase(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.DO_NOTHING, related_name="purchase"
    )
    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING, related_name="+")

    def save(self, *args, **kwargs):
        super(Purchase, self).save(*args, **kwargs)
        self.user.buyback_count()
