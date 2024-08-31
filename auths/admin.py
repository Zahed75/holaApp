from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'otp_verified') 

admin.site.register(UserProfile, UserProfileAdmin)
