# Generated by Django 2.2.13 on 2020-10-20 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aries_community', '0019_ariesuser_pubkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='ariesuser',
            name='cidade_emissao',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='ariesuser',
            name='estado',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='ariesuser',
            name='estado_emissao',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='ariesuser',
            name='inss',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='ariesuser',
            name='natural',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='ariesuser',
            name='rg',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='ariesuser',
            name='secao',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='ariesuser',
            name='titulo',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='ariesuser',
            name='zona',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='ariesuser',
            name='cpf',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
