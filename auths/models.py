from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid  # Add this import to generate a unique ID

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('outlet_manager', 'Outlet Manager'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_user_id = models.CharField(max_length=36, unique=True, editable=False)  # New field for unique ID
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=4)
    otp_created_at = models.DateTimeField(default=timezone.now)
    otp_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate a unique ID if it doesn't exist
        if not self.unique_user_id:
            self.unique_user_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def is_otp_valid(self, otp):
        # Check if OTP matches and is within the 5-minute validity period
        return (self.otp == otp and 
                self.otp_created_at >= timezone.now() - timedelta(minutes=5))

    def __str__(self):
        return self.phone_number
