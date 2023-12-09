from django.db import models
from django import forms


# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=128)

    address = models.CharField(max_length=2000, default="")


    map_adress = models.CharField(max_length=2000, default="")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "building"

    def __str__(self):
        return self.name

class Area(models.Model):
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name="area" 
    )

    name = models.CharField(max_length=50)

    has_balcony = models.BooleanField(default=False)
    has_sitting = models.BooleanField(default=False)
    has_dance_floor = models.BooleanField(default=False)

    capacity_balcony = models.IntegerField(default=0)
    capacity_sitting = models.IntegerField(default=0)
    capacity_dance_floor = models.IntegerField(default=0)

    class Meta:
        db_table = "areas"

    def __str__(self) -> str:
        return f"{self.building.name} | {self.name}"
