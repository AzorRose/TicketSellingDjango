from django.db import models
from django.contrib.auth.models import User
from apps.events.models import Ticket
from django.utils import timezone
from datetime import date
from django.contrib.postgres.fields import ArrayField


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name="profile"
    )

    first_name = models.CharField(max_length=32, blank=True, default="")
    second_name = models.CharField(max_length=32, blank=True, default="")
    gender = models.CharField(max_length=9, blank=True, default="")
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    balance = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    buyback_sum = models.FloatField(default=0)

    basket = ArrayField(base_field=models.CharField(default=""), blank=True, null=True)

    bonus_levels = {5000: 0, 10000: 2, 30000: 5, float("inf"): 10}

    def count_buyback(self):
        purchases = Purchase.objects.filter(user=self)

        self.buyback_sum = sum([i.ticket.price for i in purchases])

        self.save(update_fields=["buyback_sum"])
        self.count_bonus()

    def count_bonus(self):
        for i in self.bonus_levels:
            if self.buyback_sum < i:
                self.bonus = self.bonus_levels[i]
                self.save(update_fields=["bonus"])
                break
        
    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
    
    @property
    def get_basket(self):
        basket_ids = self.basket
        basket = []

        purchases = Purchase.objects.filter(id__in=basket_ids)

        for purchase in purchases:
            basket.append(purchase)

        return basket
    
    @property
    def basket_sum(self) -> float:
        total = sum([i.ticket.price for i in self.get_basket])
        return total - total * (self.bonus / 100) if self.bonus != 0 else total
    
    @property
    def have_money(self):
        return self.balance >= self.basket_sum

    def buy(self):
        if self.have_money:
            for i in self.get_basket:
                if i.have_place():
                    # Подтвердить покупку
                    i.make_completed()
                    # Изменение общего количества людей
                    i.ticket.event.change_people_count(True)
                    # Изменение количества людей на конкретный тип места
                    i.ticket.event.change_spot_count(i.ticket.spot, True)
                    # Бронь конкретного места
                    i.ticket.event.booked_places["items"][i.ticket.spot][str(i.spot_row)][str(i.spot_num)]["available"] = False
                    i.ticket.event.save()                  
                    # Установка времени покупки билета
                    i.creation_time = timezone.now()
                    super(Purchase, i).save()
            
        self.balance -= self.basket_sum
        self.basket.clear()
        self.save(update_fields=["balance", "basket"])
        self.count_buyback()
            
    def add_balance(self, num):
        self.balance += num
        self.save(update_fields=["balance"])

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        db_table = "Users"
        verbose_name_plural = "Профили пользователей"
        verbose_name = "профиль пользователя"

    def get_empty_user_profile():
        return UserProfile.objects.get(user=User.objects.get(username="empty"))
    
class Purchase(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_DEFAULT,
        related_name="purchase",
        default=UserProfile.get_empty_user_profile,
    )

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="ticket")

    creation_time = models.DateTimeField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    spot_num = models.IntegerField(default=0)
    
    spot_row = models.IntegerField(default=0)

    def add_to_basket(self):
        if self.have_place() and self.id not in self.user.get_basket:
            self.user.basket.append(self.id)
            self.user.save(update_fields=["basket"])

    def have_place(self) -> bool:
        has_place = (
            True
            if (
                self.ticket.spot == "seat"
                and self.ticket.event.place.capacity_sitting
                > self.ticket.event.booked_seat
            )
            or (
                self.ticket.spot == "balcony"
                and self.ticket.event.place.capacity_balcony
                > self.ticket.event.booked_balcony
            )
            or (
                self.ticket.spot == "dance_floor"
                and self.ticket.event.place.capacity_dance_floor
                > self.ticket.event.booked_dance_floor
            )
            else False
        )

        ticket = self.ticket
        event = ticket.event

        if ticket.spot == "dance_floor":
            return has_place

        is_available = True if event.booked_places["items"][ticket.spot][str(self.spot_row)][str(self.spot_num)]["available"] else False

        return has_place and is_available

    def make_completed(self):
        self.completed = True
        self.save(update_fields=["completed"])

    def save(self, *args, **kwargs):
        if not self.id:
            super(Purchase, self).save(*args, **kwargs)
            self.add_to_basket()
        super(Purchase, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.completed:
            self.ticket.event.change_people_count(False)
        super(Purchase, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Покупки"
        verbose_name = "объект"
