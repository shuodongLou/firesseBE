# Generated by Django 2.0.1 on 2018-03-16 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireserv', '0016_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
