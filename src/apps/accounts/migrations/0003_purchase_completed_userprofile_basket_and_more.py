# Generated by Django 5.0 on 2023-12-09 16:22

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchase",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="basket",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(default=""),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="first_name",
            field=models.CharField(blank=True, default="", max_length=32),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="gender",
            field=models.CharField(blank=True, default="", max_length=9),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="second_name",
            field=models.CharField(blank=True, default="", max_length=32),
        ),
    ]
