# Generated by Django 4.1.1 on 2022-09-22 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0002_payment_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="date_completed",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
