from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # How many empty forms to display by default

class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderId', 'customer', 'amount', 'status', 'orderTime')
    inlines = [OrderItemInline]

    def customer(self, obj):
        return obj.customer.phone_number

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
