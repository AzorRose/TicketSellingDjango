from django.db import models

# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=128)
    
    address = models.CharField(max_length=256, default="")
    
    class Meta:
        db_table = "building"

    def __str__(self):
        return self.name

class Area(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="area")
    
    name = models.CharField(max_length=50)
    
    capacity_balcony = models.IntegerField(default=0)
    capacity_sitting = models.IntegerField(default=0)
    capacity_dance_floor = models.IntegerField(default=0)
    
    class Meta:
        db_table = "areas"
