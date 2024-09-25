from django.contrib import admin
from .models import *

# Define the InventoryInline to use in ProductAdmin
class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1  # Number of empty forms displayed to add new inventories
    min_num = 1  # Minimum number of inventory entries required
    max_num = 10  # Maximum number of inventory entries allowed
    verbose_name = 'Inventory'
    verbose_name_plural = 'Inventories'


# Register Product and InventoryAdmin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','productName', 'regularPrice', 'salePrice', 'saleStart', 'saleEnd')
    search_fields = ('productName', 'productDescription', 'seoTitle')
    inlines = [InventoryInline]  # Add InventoryInline to ProductAdmin


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id','product', 'size', 'quantity', 'barCode', 'available')
    search_fields = ('product__productName', 'size', 'barCode')
    ordering = ('product', 'size')
    list_filter = ('available',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')