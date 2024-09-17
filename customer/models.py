# customer/models.py
from django.db import models
from auths.models import *

class Customer(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    wishlist = models.TextField(blank=True, null=True)
    club_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.email

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='shipping_addresses')
    name = models.CharField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(max_length=500)
    area = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.customer.name} - {self.phone_number}'
