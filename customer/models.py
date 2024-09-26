# customer/models.py
from django.db import models
from django.contrib.auth.models import User  # Ensure correct import

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    wishlist = models.TextField(blank=True, null=True)
    club_points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='shipping_addresses')
    name = models.CharField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    area = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.customer.name} - {self.phone_number}'
