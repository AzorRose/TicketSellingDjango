# Generated by Django 4.2.5 on 2023-11-01 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0005_alter_event_table_tickets"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tickets",
            name="events",
        ),
        migrations.AddField(
            model_name="tickets",
            name="event",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ticket",
                to="events.event",
            ),
        ),
        migrations.AddField(
            model_name="tickets",
            name="price",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="tickets",
            name="spot",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AlterModelTable(
            name="tickets",
            table="tickets",
        ),
    ]
