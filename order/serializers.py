from rest_framework import serializers
from .models import *
from decimal import Decimal



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price','size', 'color']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'id', 'user', 'status', 'payment_method', 'shipping_cost', 'total_price', 'vat', 'grand_total', 'order_items',
                  'created_at', 'updated_at']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)

        # Process order items
        total_price = 0
        for item_data in order_items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            # Choose price based on business logic (offer price vs regular price)
            price = product.regularPrice if validated_data.get('use_coupon') else product.salePrice
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total_price += price * quantity

        # Calculate totals
        order.total_price = total_price
        order.vat = total_price * Decimal(0.05)  # Assuming VAT is 5%
        order.grand_total = total_price + order.shipping_cost + order.vat

        order.save()
        return order
