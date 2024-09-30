from rest_framework import serializers
from wishlist.models import Wishlist
from products.models import *
# serializers.py



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'productName', 'productDescription', 'regularPrice', 'salePrice', 'featureImage']  # Add fields as necessary

class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.ListField(child=serializers.IntegerField(), write_only=True)  # Accept a list of product IDs

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        product_ids = validated_data.pop('products')  # Get the list of product IDs
        user = self.context['request'].user  # Get the logged-in user
        validated_data.pop('user', None)  # Remove 'user' if it exists

        # Create a wishlist item for each product ID
        wishlist_items = []
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            wishlist_item = Wishlist.objects.create(user=user.userprofile, product=product)
            wishlist_items.append(wishlist_item)

        return wishlist_items  # Return the list of created wishlist items
