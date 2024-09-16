from django.contrib import admin
from .models import Order



class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'customerName', 'customerPhoneNumber', 'orderTime', 'amount', 'orderStatus', 'status']
    search_fields = ['orderId', 'customerName', 'customerPhoneNumber']  # Search by customer name and phone number
    list_filter = ['orderStatus', 'status']

admin.site.register(Order, OrderAdmin)
