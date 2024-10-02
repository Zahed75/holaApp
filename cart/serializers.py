# cart/serializers.py
from rest_framework import serializers
from .models import Cart
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Serialize the product details
    total_price = serializers.ReadOnlyField()  # Read-only field for total price

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'total_price', 'added_at']

    def create(self, validated_data):
        customer = validated_data['customer']
        product = validated_data['product']
        quantity = validated_data['quantity']

        # Check if the product is already in the cart, update the quantity if it is
        cart_item, created = Cart.objects.update_or_create(
            customer=customer,
            product=product,
            defaults={'quantity': quantity}
        )
        return cart_item
