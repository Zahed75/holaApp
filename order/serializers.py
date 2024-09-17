from rest_framework import serializers
from .models import *
from products.models import  *
from customer.models import *


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

    def validate(self, data):
        # Ensure the product exists and has a price
        if not Product.objects.filter(id=data['product'].id).exists():
            raise serializers.ValidationError("Product does not exist.")
        if data['price'] is None:
            raise serializers.ValidationError("Price cannot be null.")
        return data

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    shippingAddress = serializers.PrimaryKeyRelatedField(queryset=ShippingAddress.objects.all())

    class Meta:
        model = Order
        fields = ['user', 'status', 'shippingAddress', 'shipping_cost', 'order_items']

    def create(self, validated_data):
        # Extract order items from validated data
        order_items_data = validated_data.pop('order_items')
        # Create the Order instance
        order = Order.objects.create(**validated_data)
        # Create OrderItem instances
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        # Recalculate totals
        order.calculate_totals()
        return order