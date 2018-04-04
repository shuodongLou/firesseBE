# Generated by Django 2.0.1 on 2018-03-23 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fireserv', '0026_auto_20180322_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=100)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='fireserv.Order')),
            ],
        ),
    ]