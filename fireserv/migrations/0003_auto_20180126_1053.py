# Generated by Django 2.0.1 on 2018-01-26 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireserv', '0002_auto_20180122_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='account',
            name='sex',
            field=models.CharField(blank=True, default='', max_length=5),
        ),
    ]
