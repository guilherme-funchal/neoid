# Generated by Django 2.2.13 on 2020-10-01 12:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aries_community', '0016_auto_20200924_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentconversation',
            name='creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
