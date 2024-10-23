from django.contrib import admin
from .models import *


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1
    min_num = 1
    max_num = 10
    verbose_name = 'Inventory'
    verbose_name_plural = 'Inventories'



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','productName', 'regularPrice', 'salePrice', 'saleStart', 'saleEnd')
    search_fields = ('productName', 'productDescription', 'seoTitle')
    inlines = [InventoryInline]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id','product', 'size', 'quantity', 'barCode', 'available')
    search_fields = ('product__productName', 'size', 'barCode')
    ordering = ('product', 'size')
    list_filter = ('available',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')