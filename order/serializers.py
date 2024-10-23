from rest_framework import serializers
from .models import *
from decimal import Decimal
from customer.serializers import *
from products.serializers import *




class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'size', 'color']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = CustomerSerializer(source='user.customer', read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'id', 'user', 'status', 'payment_method', 'shipping_cost',
            'total_price', 'vat', 'grand_total', 'order_items', 'shipping_address',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        shipping_address_id = request.data.get('shipping_address_id')
        coupon_code = request.data.get('coupon_code')

        # Ensure the shipping address is valid
        try:
            shipping_address = ShippingAddress.objects.get(id=shipping_address_id, customer__user=user)
        except ShippingAddress.DoesNotExist:
            raise serializers.ValidationError({'shipping_address': 'Invalid shipping address'})

        # Create the order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            payment_method=validated_data.get('payment_method'),
            shipping_cost=validated_data.get('shipping_cost', Decimal(0))
        )

        # Process order items
        items_data = request.data.get('items')
        total_price = 0
        use_regular_price = coupon_code is not None  # Use regular price if coupon is applied

        for item_data in items_data:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity')
            size = item_data.get('size')
            color = item_data.get('color')

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product': f'Product with ID {product_id} not found'})

            # If a coupon is applied, use regularPrice; otherwise, use salePrice if active
            if use_regular_price:
                price = product.regularPrice
            else:
                current_date = timezone.now()
                if product.sale_start <= current_date <= product.sale_end:
                    price = product.salePrice
                else:
                    price = product.regularPrice

            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price, size=size, color=color)
            total_price += price * quantity

        # Apply coupon logic if a coupon is provided
        discount_amount = 0
        if coupon_code:
            try:
                discount = Discount.objects.get(code=coupon_code)

                # Check if the coupon is still valid
                if discount.coupon_expiry and discount.coupon_expiry < timezone.now().date():
                    raise serializers.ValidationError({'coupon_code': 'Coupon has expired'})

                # Check if minimum spend requirement is met
                if discount.minimum_spend and total_price < discount.minimum_spend:
                    raise serializers.ValidationError({'coupon_code': 'Minimum spend not met to apply this coupon'})

                # Check if user is blocked from using this coupon
                if user in discount.blocked_accounts.all():
                    raise serializers.ValidationError({'coupon_code': 'You are not allowed to use this coupon'})

                # Apply discount
                discount_amount = discount.coupon_amount
                total_price -= discount_amount  # Deduct discount from total price
                order.coupon_code = discount

                # Free shipping if allowed by the coupon
                if discount.allow_free_shipping:
                    order.shipping_cost = 0

            except Discount.DoesNotExist:
                raise serializers.ValidationError({'coupon_code': 'Invalid coupon code'})

        # Calculate VAT and grand total
        vat_rate = Decimal(0.05)  # Assuming a VAT rate of 5%
        vat_amount = total_price * vat_rate
        grand_total = total_price + vat_amount + order.shipping_cost

        # Set the final values in the order
        order.total_price = total_price
        order.vat = vat_amount
        order.grand_total = grand_total

        # Save the order
        order.save()

        return order







class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'phone_number', 'address', 'area', 'street', 'city', 'state', 'zip_code']
