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
    balance = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    buyback_sum = models.FloatField(default=0)

    bonus_levels = {5000: 0, 10000: 2, 30000: 5, float("inf"): 10}
    
    def count_buyback(self):
        purchases = Purchase.objects.filter(user=self)
        summary = 0
        for i in purchases:
            summary += i.ticket.price
        self.buyback_sum = summary
        self.save(update_fields=["buyback_sum"])
        self.count_bonus()

    def count_bonus(self):
        for i in self.bonus_levels:
            if self.buyback_sum < i:
                self.bonus = self.bonus_levels[i]
                break
        self.save(update_fields=["bonus"])

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def add_balance(self, num):
        self.balance += num
        self.save(update_fields=["balance"])

    def get_balance(self):
        return self.balance
    
    def __str__(self) -> str:
        return self.user.username
            
    class Meta:
        db_table = "Users"
        
    def get_default_user_profile():
        return UserProfile.objects.get(user=User.objects.get(username="empty"))


class Purchase(models.Model):
    
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_DEFAULT, related_name="purchase", default=UserProfile.get_default_user_profile)

    ticket = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING, related_name="ticket")

    def can_buy_ticket(self) -> bool:
        return True if self.user.get_balance() >= self.ticket.price else False
        
    def buy_ticket(self):
        self.user.balance -= self.ticket.price
        self.user.save()
                
    def save(self, *args, **kwargs):
        if self.can_buy_ticket():
            self.buy_ticket() 
            super(Purchase, self).save(*args, **kwargs)
            self.user.count_buyback()
        else:
            raise Exception("no money")
