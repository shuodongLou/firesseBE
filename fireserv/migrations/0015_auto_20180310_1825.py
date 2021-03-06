# Generated by Django 2.0.1 on 2018-03-10 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireserv', '0014_auto_20180309_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='effects',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='product',
            name='ingredients',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='product',
            name='notes',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='product',
            name='usage',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
