from django.contrib import admin
from .models import Product, Inventory


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productName', 'regularPrice', 'salePrice', 'saleStart', 'saleEnd')
    search_fields = ('productName', 'productDescription', 'seoTitle')





@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity', 'barCode', 'available')
    search_fields = ('product__productName', 'size', 'barCode')
    ordering = ('product', 'size')
    list_filter = ('available',)
