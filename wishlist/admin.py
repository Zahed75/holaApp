from django.contrib import admin
from .models import Wishlist

# Register your models here.


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'product', 'created_at')  # Fields to display in the list view
    search_fields = ('user__phone_number', 'product__productName')  # Enable searching by user phone number or product name
    list_filter = ('user', 'product')  # Add filters for user and product
    ordering = ('-created_at',)  # Order by creation date descending

    def __str__(self):
        return f"{self.user.phone_number}'s wishlist"

