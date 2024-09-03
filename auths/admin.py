from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number','user', 'role', 'otp_verified') 

admin.site.register(UserProfile, UserProfileAdmin)
