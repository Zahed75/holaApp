from django.contrib import admin
from .models import *


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'dob', 'club_points')
    search_fields = ('name', 'email')
    inlines = [ShippingAddressInline]

admin.site.register(Customer, CustomerAdmin)