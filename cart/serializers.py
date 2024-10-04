# cart/serializers.py
from rest_framework import serializers
from .models import Cart
from products.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'color', 'size', 'quantity', 'total_price', 'added_at']

    def create(self, validated_data):
        customer = validated_data['customer']
        product = validated_data['product']
        quantity = validated_data['quantity']
        color = validated_data.get('color')
        size = validated_data.get('size')

        # Check if the product is already in the cart, update if it is
        cart_item, created = Cart.objects.update_or_create(
            customer=customer,
            product=product,
            color=color,
            size=size,
            defaults={'quantity': quantity}
        )
        return cart_item
