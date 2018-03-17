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
    username = models.CharField(max_length=20, blank=True, default='')
    time_created = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20)
    fire_code = models.CharField(max_length=10, blank=True, default='')
    level = models.PositiveIntegerField(default=0)
    province = models.CharField(max_length=15, blank=True, default='')
    city = models.CharField(max_length=15, blank=True, default='')
    county = models.CharField(max_length=15, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    name = models.CharField(max_length=20, blank=True, default='')
    sex = models.CharField(max_length=5, blank=True, default='')
    birthday = models.DateField(blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)
    skin_type = models.CharField(max_length=100, blank=True, default='')
    skin_notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('time_created',)

class Photo(models.Model):
    account = models.ForeignKey(Account, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')
    timestamp = models.DateTimeField(auto_now_add=True)
    inquiry_id = models.PositiveIntegerField(default=0, editable=True)



class Inquiry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, related_name='inquiries', on_delete=models.CASCADE)
    note = models.TextField(blank=True, default='')
    status = models.BooleanField(blank=True, default=False)
    reply = models.TextField(blank=True, default='')
    subtypea1 = models.PositiveIntegerField(default=0)
    subtypea2 = models.PositiveIntegerField(default=0)
    subtypea3 = models.PositiveIntegerField(default=0)
    subtypeb1 = models.PositiveIntegerField(default=0)
    subtypeb2 = models.PositiveIntegerField(default=0)
    subtypeb3 = models.PositiveIntegerField(default=0)
    subtypec1 = models.PositiveIntegerField(default=0)
    subtypec2 = models.PositiveIntegerField(default=0)
    subtypec3 = models.PositiveIntegerField(default=0)
    subtyped1 = models.PositiveIntegerField(default=0)
    subtyped2 = models.PositiveIntegerField(default=0)
    subtyped3 = models.PositiveIntegerField(default=0)
    subtypee1 = models.PositiveIntegerField(default=0)
    subtypee2 = models.PositiveIntegerField(default=0)

class Product(models.Model):
    name = models.CharField(max_length=200)
    name_e = models.CharField(max_length=200, default='', blank=True)
    desc = models.TextField(blank=True, default='')
    series = models.CharField(max_length=200, default='', blank=True)
    status = models.CharField(max_length=20, default='', blank=True)
    price = models.PositiveIntegerField(default=0)
    inventory = models.PositiveIntegerField(default=100)
    histsales = models.PositiveIntegerField(default=0)
    volume = models.CharField(max_length=10, default='', blank=True)
    effects = models.CharField(max_length=1000, default='', blank=True)
    ingredients = models.CharField(max_length=500, default='', blank=True)
    usage = models.CharField(max_length=1000, default='', blank=True)
    notes = models.CharField(max_length=500, default='', blank=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimage/')

class Agent(models.Model):
    acct_id = models.IntegerField(default=-1)
    fire_code = models.CharField(max_length=10, blank=False, default='000000')
    fire_points = models.PositiveIntegerField(default=0)
    commission_rate = models.PositiveIntegerField(default=0)
    t_sales = models.PositiveIntegerField(default=0)
    y_sales = models.PositiveIntegerField(default=0)
    m_sales = models.PositiveIntegerField(default=0)
    t_commission = models.PositiveIntegerField(default=0)
    y_commission = models.PositiveIntegerField(default=0)
    m_commission = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=0)
    stars = models.PositiveIntegerField(default=0)
    t_bonus = models.PositiveIntegerField(default=0)
    y_bonus = models.PositiveIntegerField(default=0)
    m_bonus = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

class Order(models.Model):
    acct_id = models.IntegerField(default=-1)
    order_id = models.CharField(max_length=20)
    time_created = models.DateTimeField(auto_now_add=True)
    time_delivered = models.DateTimeField(blank=True)
    time_resolved = models.DateTimeField(blank=True)
    product_total = models.PositiveIntegerField(default=0)
    delivery_fee = models.PositiveIntegerField(default=0)
    final_payment = models.PositiveIntegerField(default=0)
    num_of_products = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, default='PLACED')
    fire_code = models.CharField(max_length=10, blank=False, default='000000')
    cus_name = models.CharField(max_length=20, blank=True, default='')
    cus_phone = models.CharField(max_length=20, blank=True, default='')
    cus_address = models.CharField(max_length=200, blank=True, default='')
