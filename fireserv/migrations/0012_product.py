# Generated by Django 2.0.1 on 2018-03-05 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fireserv', '0011_account_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, default='')),
                ('series', models.CharField(blank=True, default='', max_length=200)),
                ('status', models.CharField(blank=True, default='', max_length=20)),
                ('price', models.PositiveIntegerField(default=0)),
                ('inventory', models.PositiveIntegerField(default=100)),
                ('histsales', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
