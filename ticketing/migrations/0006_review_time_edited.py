# Generated by Django 4.0.4 on 2022-05-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0005_alter_ticket_time_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='time_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
