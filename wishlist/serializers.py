from rest_framework import serializers
from wishlist.models import Wishlist
from products.models import *
from customer.models import *




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'productName', 'productDescription', 'regularPrice', 'salePrice', 'featureImage']

class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        product_ids = validated_data.pop('products')
        user = self.context['request'].user

        # Ensure that the authenticated user has a corresponding Customer object
        try:
            customer = Customer.objects.get(user=user)  # Fetch the customer instance
        except Customer.DoesNotExist:
            raise serializers.ValidationError("No customer profile associated with this user.")

        wishlist_items_with_products = []

        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            wishlist_item = Wishlist.objects.create(user=customer, product=product)

            wishlist_items_with_products.append({
                'id': wishlist_item.id,
                'user': wishlist_item.user.id,
                'product': ProductSerializer(product).data,
                'created_at': wishlist_item.created_at
            })

        return wishlist_items_with_products
