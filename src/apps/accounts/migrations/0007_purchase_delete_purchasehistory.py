# Generated by Django 4.2.5 on 2023-11-04 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0007_rename_tickets_ticket_alter_event_date_and_more"),
        ("accounts", "0006_purchasehistory"),
    ]

    operations = [
        migrations.CreateModel(
            name="Purchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tickets",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="events.ticket",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="purchase",
                        to="accounts.userprofile",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="PurchaseHistory",
        ),
    ]
