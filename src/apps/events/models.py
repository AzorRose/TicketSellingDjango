from django.db import models
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import post_delete


class Event(models.Model):
    name = models.CharField((""), max_length=128)
    date = models.DateTimeField((""), auto_now=False, auto_now_add=False, db_index=True)

    description = models.TextField((""))
    genre = TaggableManager()
    age_category = [
        ("0+", "0+"),
        ("6+", "6+"),
        ("12+", "12+"),
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

    def __str__(self) -> str:
        return f"{self.name} {str(self.date.day)}.{str(self.date.month)}.{str(self.date.year)} {self.date.hour}:{self.date.minute}"

    def get_absolute_url(self):
        return reverse("events:", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    class Meta:
        db_table = "events"


@receiver(post_delete, sender=Event)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        pass


class Ticket(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="ticket", default=""
    )

    price = models.FloatField(default=0)
    spot = models.CharField(max_length=50, default="")

    class Meta:
        db_table = "tickets"

    def __str__(self) -> str:
        return f"{self.event.name} ({self.price})"
