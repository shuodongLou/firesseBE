# Generated by Django 2.0.1 on 2018-03-18 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireserv', '0020_auto_20180318_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=30),
        ),
    ]
