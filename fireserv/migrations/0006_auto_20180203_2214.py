# Generated by Django 2.0.1 on 2018-02-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireserv', '0005_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]