from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20)
    fire_code = models.CharField(max_length=10, blank=True, default='')
    province = models.CharField(max_length=15, blank=True, default='')
    city = models.CharField(max_length=15, blank=True, default='')
    county = models.CharField(max_length=15, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    name = models.CharField(max_length=20, blank=True, default='')
    sex = models.CharField(max_length=5, blank=True, default='')
    birthday = models.DateField(blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    skin_type = models.CharField(max_length=100, blank=True, default='')
    skin_notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('time_created',)

class Photo(models.Model):
    account = models.ForeignKey(Account, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')
    timestamp = models.DateTimeField(auto_now_add=True)
