# Generated by Django 4.1.1 on 2022-09-20 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_alter_user_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
