# Generated by Django 4.0.4 on 2022-05-21 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userfollows',
            options={'verbose_name': 'User follow', 'verbose_name_plural': 'User follows'},
        ),
    ]
