# Generated by Django 3.2.14 on 2023-06-07 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental_app', '0006_alter_booking_car_alter_booking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='booking_queue',
            field=models.JSONField(default=list),
        ),
    ]