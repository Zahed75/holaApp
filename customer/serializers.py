from rest_framework import serializers
from .models import *
from wishlist.serializers import WishlistSerializer


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id','name', 'phone_number', 'address', 'area']

class CustomerSerializer(serializers.ModelSerializer):
    shipping_addresses = ShippingAddressSerializer(many=True, write_only=True)
    wishlist = WishlistSerializer(many=True, read_only=True, source='wishlists')
    class Meta:
        model = Customer
        fields = ['id','name', 'dob', 'email', 'club_points', 'shipping_addresses','wishlist']

    def update(self, instance, validated_data):
        shipping_addresses_data = validated_data.pop('shipping_addresses', [])

        # Update the Customer instance
        instance.name = validated_data.get('name', instance.name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.email = validated_data.get('email', instance.email)
        instance.club_points = validated_data.get('club_points', instance.club_points)
        instance.shipping_addresses = validated_data.get('shipping_addresses', instance.shipping_addresses)
        instance.save()

        # Update or create ShippingAddress instances
        for address_data in shipping_addresses_data:
            ShippingAddress.objects.update_or_create(
                customer=instance,
                phone_number=address_data.get('phone_number'),
                defaults=address_data
            )

        return instance
