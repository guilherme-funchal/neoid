# Generated by Django 2.2.13 on 2020-09-24 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aries_community', '0014_auto_20200924_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='indyproofrequest',
            name='schema',
            field=models.TextField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='indyproofrequest',
            name='agent',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
