from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from unfold.admin import ModelAdmin as unfoldModelAdmin


class UserProfileAdmin(unfoldModelAdmin):
    list_display = ('phone_number','user', 'role', 'otp_verified') 

admin.site.register(UserProfile, UserProfileAdmin)
