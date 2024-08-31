from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'otp_verified')  # Updated list_display

admin.site.register(UserProfile, UserProfileAdmin)
