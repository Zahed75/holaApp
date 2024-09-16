from django.db import models
from auths.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from auths.models import UserProfile

# Create your models here.




class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending Payment', 'Pending Payment'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Failed', 'Failed'),
    ]

    orderId = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')  # Link to UserProfile
    customerName = models.CharField(max_length=255)
    customerPhoneNumber = models.CharField(max_length=15)
    orderTime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    origin = models.CharField(max_length=255)
    orderStatus = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Pending Payment')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.orderId} - {self.customerPhoneNumber}"

