from django.contrib import admin
from .models import Customer, ShippingAddress

# Define the inline admin for ShippingAddress with the new 'name' field
class ShippingAddressInline(admin.TabularInline):
    model = ShippingAddress
    extra = 1  # Number of extra empty forms to display
    fields = ('name', 'phoneNumber', 'address', 'area')  # Include 'name' in the fields
    readonly_fields = ()  # Adjust if any fields need to be read-only

# Register the Customer admin with the inline
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customerInfo', 'email', 'dob')
    search_fields = ('customerInfo__username', 'email')
    list_filter = ('dob',)
    inlines = [ShippingAddressInline]  # Add the inline for ShippingAddress

# Optionally, register ShippingAddressAdmin separately if needed
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'name', 'phoneNumber', 'area')
    search_fields = ('customer__customerInfo__username', 'name', 'phoneNumber', 'area')
    list_filter = ('area',)
