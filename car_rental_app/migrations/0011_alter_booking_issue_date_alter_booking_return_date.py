# Generated by Django 4.2 on 2023-06-15 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental_app', '0010_remove_userprofile_gender_alter_booking_issue_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='issue_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='return_date',
            field=models.DateField(),
        ),
    ]
