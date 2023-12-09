from django.db import models
from django.contrib.auth.models import User
from apps.events.models import Ticket, Booked_Places
from django.utils import timezone
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name="profile"
    )

    first_name = models.CharField(max_length=32, blank=True)
    second_name = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=9, blank=True)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    balance = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    buyback_sum = models.FloatField(default=0)

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
                break
        self.save(update_fields=["bonus"])

    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def add_balance(self, num):
        self.balance += num
        self.save(update_fields=["balance"])

    def get_balance(self):
        return self.balance

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
 
    spot_num = models.IntegerField(default=0)

    def can_buy_ticket(self) -> bool:
        has_place = (
            True
            if (
                self.ticket.spot == "sitting"
                and self.ticket.event.place.capacity_sitting
                > self.ticket.event.booked_sitting
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

        has_money = (
            True
            if self.user.get_balance()
            >= self.ticket.price - (self.ticket.price * (self.user.bonus / 100))
            else False
        )

        is_available = Booked_Places.objects.get(
            spot_num=self.spot_num, spot=self.ticket.spot
        ).available

        return has_money and has_place and is_available

    def buy_ticket(self):
        self.user.balance -= self.ticket.price - (
            self.ticket.price * (self.user.bonus / 100)
        )
        self.user.save(update_fields=["balance"])

    def save(self, *args, **kwargs):
        if not self.id:
            if self.can_buy_ticket():
                # Вычет баланса
                self.buy_ticket()
                # Изменение общего количества людей
                self.ticket.event.change_people_count(True)
                # Изменение количества людей на конкретный тип места
                self.ticket.event.change_spot_count(self.ticket.spot, True)
                # Бронь конкретного места
                temp = Booked_Places.objects.get(
                    spot_num=self.spot_num, spot=self.ticket.spot
                )
                temp.available = False
                temp.user = self.user
                temp.save()
                # Установка времени покупки билета
                self.creation_time = timezone.now()
                print(self.creation_time, *args, **kwargs)
                super(Purchase, self).save(*args, **kwargs)
                # Подсчет новой суммы выкупа пользователя для получения скидки
                self.user.count_buyback()
                return
            else:
                raise Exception("can`t buy it")
        super(Purchase, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.ticket.event.change_people_count(False)
        super(Purchase, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Покупки"
        verbose_name = "объект"
