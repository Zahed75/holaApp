# auths/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Base model for common fields
class BaseUser(models.Model):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional for customers
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    otp_verified = models.BooleanField(default=False)  # Optional for admin users
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    class Meta:
        abstract = True

# Manager for creating users and superusers
class UserManager(BaseUserManager):
    def create_user(self, email, password, full_name, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, full_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, full_name, **extra_fields)

# Admin user model
class AdminUser(AbstractBaseUser, BaseUser):
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

# Customer model
class Customer(BaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.full_name

# OutletManager model
class OutletManager(BaseUser):
    email = models.EmailField(unique=True)  # Ensure unique email for outlet managers
    
    class Meta:
        verbose_name = 'Outlet Manager'
        verbose_name_plural = 'Outlet Managers'

    def __str__(self):
        return self.full_name
