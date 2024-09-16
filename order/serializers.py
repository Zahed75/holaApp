from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'vat', 'shipping_cost', 'grand_total', 'order_items', 'created_at', 'updated_at']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)

        order.calculate_total()
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)

        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if order_items_data:
            instance.order_items.all().delete()
            for order_item_data in order_items_data:
                OrderItem.objects.create(order=instance, **order_item_data)

        instance.calculate_total()
        return instance
