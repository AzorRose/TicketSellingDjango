# Generated by Django 4.2.6 on 2023-12-17 20:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0002_event_booked_places"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Booked_Places",
        ),
    ]