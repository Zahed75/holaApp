from django.contrib import admin
from .models import *



class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'dob', 'club_points')
    search_fields = ('name', 'email')

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'name', 'phone_number', 'address', 'city', 'state', 'zip_code')
    search_fields = ('name', 'phone_number', 'customer__name')  # Enable searching by customer's name

admin.site.register(Customer, CustomerAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
