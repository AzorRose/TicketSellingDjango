# Generated by Django 4.2.5 on 2023-11-12 08:08

import apps.accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
        ("accounts", "0003_userprofile_age_alter_userprofile_balance_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="age",
        ),
        migrations.AlterField(
            model_name="purchase",
            name="ticket",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="ticket",
                to="events.ticket",
            ),
        ),
        migrations.AlterField(
            model_name="purchase",
            name="user",
            field=models.ForeignKey(
                default=apps.accounts.models.UserProfile.get_default_user_profile,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="purchase",
                to="accounts.userprofile",
            ),
        ),
    ]
