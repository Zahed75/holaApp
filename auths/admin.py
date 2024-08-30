from django.contrib import admin

# Register your models here.
# auths/admin.py

from django.contrib import admin
from .models import AdminUser, Customer, OutletManager

class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'full_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'is_active', 'date_joined')
    search_fields = ('email', 'full_name', 'phone_number')
    list_filter = ('is_active',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

class OutletManagerAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'date_joined')
    search_fields = ('email', 'full_name')
    list_filter = ('is_active',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)
    

# Register models with admin site
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(OutletManager, OutletManagerAdmin)
