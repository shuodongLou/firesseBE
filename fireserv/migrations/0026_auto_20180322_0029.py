# Generated by Django 2.0.1 on 2018-03-22 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireserv', '0025_auto_20180322_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='articlecovers/'),
        ),
    ]