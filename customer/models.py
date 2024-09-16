from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    customerInfo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customerInfo')
    email = models.EmailField(max_length=254, unique=True)
    dob = models.DateField()

    def __str__(self):
        return str(self.customerInfo)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='shipping_addresses')
    name = models.CharField(max_length=254,blank=True,null=True)
    phoneNumber = models.CharField(max_length=20, unique=True)
    address = models.TextField(max_length=500)
    area = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.customer} - {self.phoneNumber}'
