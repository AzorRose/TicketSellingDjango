import os
from django.db import models
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import post_delete
from datetime import date
from apps.buildings.models import Area
from django.urls import reverse
from django.db.models import JSONField
from utils import places_json
from django.contrib.postgres.fields import ArrayField

class Event(models.Model):
    name = models.CharField((""), max_length=128)
    end_date = models.DateTimeField(
        (""), auto_now=False, auto_now_add=False, db_index=True
    )
    description = models.TextField((""))
    genre = TaggableManager()
    age_category = [
        ("0+", "0+"),
        ("6+", "6+"),
        ("12+", "12+"),
        ("14+", "14+"),
        ("16+", "16+"),
        ("18+", "18+"),
    ]

    ages = models.CharField(max_length=3, choices=age_category, default="0+")
    image = models.ImageField(
        (""),
        upload_to="apps/events/static/img",
        height_field=None,
        width_field=None,
        max_length=None,
    )
    slug = models.SlugField(
        verbose_name="url мероприятия", max_length=255, blank=True, unique=True
    )
    people_count = models.IntegerField(default=0)
        
    booked_balcony = models.IntegerField(default=0)
    booked_seat = models.IntegerField(default=0)
    booked_dance_floor = models.IntegerField(default=0)
    
    place = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="event", null=True)
    
    booked_places = JSONField(null = True, blank = True)
    
    filters = [
        ("all", "all"),
        ("sport", "sport"),
        ("concerts", "concerts"),
        ("festivals", "festivals"),
        ("kids", "kids"),
    ]    
    filter = models.CharField(max_length=50, choices=filters, default="all")

    def change_people_count(self, change):
        if change:
            self.people_count += 1
        else:
            self.people_count -= 1
        self.save()
    
    def change_spot_count(self, spot, change):
        if change:
            exec(f"self.booked_{spot} += 1")
        else:
            exec(f"self.booked_{spot} -= 1")
        self.save()
    def __str__(self) -> str:
        return f"{self.name} {str(self.end_date.day)}.{str(self.end_date.month)}.{str(self.end_date.year)} {self.end_date.hour}:{self.end_date.minute}"

    def get_absolute_url(self):
        return reverse("events:", kwargs={"slug": self.slug})


    def save(self, *args, **kwargs):
        if not self.id:
            file_path = os.path.join('.\\apps\events\static\main\schemas\Frame.svg')
            self.booked_places = places_json(file_path)

        if not self.slug:
            self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    @property
    def is_available(self):
        return not self.is_expired or self.people_count < self.place.capacity_dance_floor + self.place.capacity_balcony + self.place.capacity_sitting

    @property
    def is_expired(self):
        return date.today() > self.end_date

    class Meta:
        db_table = "events"
        verbose_name_plural = "События"
        verbose_name = "событие"

@receiver(post_delete, sender=Event)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket")

    price = models.FloatField(default=0)
    
    spots = [
        ("seat", "seat"),
        ("balcony", "balcony"),
        ("dance_floor", "dance_floor"),
    ]    
    
    spot = models.CharField(max_length=50, choices=spots, null=True, blank=True)

    rows = ArrayField(base_field=models.IntegerField(), default=[])
    
    def save(self, *args, **kwargs):
        if not self.id:
            super(Ticket, self).save()
            for i in self.rows: 
                temp = self.event.booked_places["items"][self.spot][str(i)]
                for j in temp:
                    print(j)
                    temp[j]["ticket"] = self.id
            self.event.save(update_fields=["booked_places"])
        super(Ticket, self).save()
    class Meta:
        db_table = "tickets"

    def __str__(self) -> str:
        return f'{self.event.name} ({self.price})'

    class Meta:
        verbose_name_plural = "Билеты"
        verbose_name = "билет"
    
    