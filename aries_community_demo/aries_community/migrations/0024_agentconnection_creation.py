# Generated by Django 2.2.13 on 2020-10-27 17:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aries_community', '0023_auto_20201027_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentconnection',
            name='creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
