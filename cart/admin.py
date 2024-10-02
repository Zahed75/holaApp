# cart/admin.py
from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'product', 'quantity', 'total_price', 'added_at')
    search_fields = ('customer__name', 'product__productName')
    list_filter = ('added_at',)

admin.site.register(Cart, CartAdmin)
