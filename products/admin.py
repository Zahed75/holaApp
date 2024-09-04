from django.contrib import admin
from .models import Product, Inventory
from unfold.admin import ModelAdmin as unfoldModelAdmin

class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1

@admin.register(Product)
class ProductAdmin(unfoldModelAdmin):
    list_display = ('id','productName', 'category', 'regularPrice', 'salePrice', 'weight',)

    search_fields = ('productName', 'seoTitle', 'seoDescription')

    list_filter = ('regularPrice', 'salePrice', 'weight', 'category')
    
    inlines = [InventoryInline]
    
    fieldsets = (
        ('General Information', {
            'fields': ('category', 'productName', 'featureImage', 'productsGallery', 
                       'productDescription', 'seoTitle', 'seoDescription', 
                       'productShortDescription')
        }),
        ('Pricing', {
            'fields': ('regularPrice', 'salePrice', 'saleStart', 'saleEnd')
        }),
        ('Inventory', {
            'fields': ('sizeCharts', 'fabric')
        }),
        ('Shipping', {
            'fields': ('weight', 'dimension_length', 'dimension_width', 'dimension_height')
        }),
    )




@admin.register(Inventory)
class InventoryAdmin(unfoldModelAdmin):
    list_display = ('product', 'size', 'quantity', 'barCode', 'available')
    search_fields = ('product__productName', 'size', 'barCode')
    ordering = ('product', 'size')
    list_filter = ('available',)


