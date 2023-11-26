# Generated by Django 4.2.5 on 2023-11-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("buildings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="building",
            name="address",
            field=models.CharField(default="", max_length=256),
        ),
        migrations.AlterField(
            model_name="building",
            name="name",
            field=models.CharField(max_length=128),
        ),
        migrations.AlterModelTable(
            name="building",
            table="building",
        ),
    ]
