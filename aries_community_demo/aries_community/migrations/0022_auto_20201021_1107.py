# Generated by Django 2.2.16 on 2020-10-21 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aries_community', '0021_auto_20201020_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ariesuser',
            name='cpf',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
