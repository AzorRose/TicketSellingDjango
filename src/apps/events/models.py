from django.db import models
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import post_delete
from datetime import date
from apps.buildings.models import Area


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
    booked_sitting = models.IntegerField(default=0)
    booked_dance_floor = models.IntegerField(default=0)

    place = models.ForeignKey(
        Area, on_delete=models.CASCADE, related_name="event", null=True
    )

    filters = [
        ("all", "all"),
        ("sport", "sport"),
        ("concerts", "concerts"),
        ("festivals", "festivals"),
        ("kids", "kids"),
    ]
    filter = models.CharField(max_length=50, choices=filters, default="all")

    async def change_people_count(self, change):
        if change:
            self.people_count += 1
        else:
            self.people_count -= 1
        self.save()

    async def change_spot_count(self, spot, change):
        if change:
            exec(f"self.booked_{spot} += 1")
        else:
            exec(f"self.booked_{spot} -= 1")
        self.save()

    def __str__(self) -> str:
        return f"{self.name} {str(self.end_date.day)}.{str(self.end_date.month)}.{str(self.end_date.year)} {self.end_date.hour}:{self.end_date.minute}"

    def get_absolute_url(self):
        return reverse("events:", kwargs={"slug": self.slug})

    async def new_event_places(self, capacity, spot):
        for i in range(capacity):
            place = Booked_Places.objects.create(
                event=self, spot=spot, spot_num=i + 1, available=True
            )
            place.save()

    def save(self):
        redact = False
        if not self.id:
            redact = True
        if not self.slug:
            self.slug = slugify(self.name)
        super(Event, self).save()
        if redact:
            if self.place.has_balcony:
                self.new_event_places(self.place.capacity_balcony, "balcony")
            if self.place.has_sitting:
                self.new_event_places(self.place.capacity_sitting, "sitting")
            if self.place.has_dance_floor:
                self.new_event_places(self.place.capacity_dance_floor, "dance_floor")

    @property
    def is_available(self):
        return (
            not self.is_expired
            or self.people_count
            < self.place.capacity_dance_floor
            + self.place.capacity_balcony
            + self.place.capacity_sitting
        )

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
        ("sitting", "sitting"),
        ("balcony", "balcony"),
        ("dance_floor", "dance_floor"),
    ]

    spot = models.CharField(max_length=50, choices=spots, null=True, blank=True)

    class Meta:
        db_table = "tickets"

    def __str__(self) -> str:
        return f"{self.event.name} ({self.price})"

    class Meta:
        verbose_name_plural = "Билеты"
        verbose_name = "билет"


class Booked_Places(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="available")

    spots = [
        ("sitting", "sitting"),
        ("balcony", "balcony"),
        ("dance_floor", "dance_floor"),
    ]

    spot = models.CharField(max_length=50, choices=spots, null=True, blank=True)

    spot_num = models.IntegerField(default=0)

    available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (
            f"{self.event} ({self.spot} | {self.spot_num}) available: {self.available}"
        )
