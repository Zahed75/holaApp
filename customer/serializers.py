from rest_framework import serializers
from .models import *



class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'phone_number', 'address', 'area']

class CustomerSerializer(serializers.ModelSerializer):
    shipping_addresses = ShippingAddressSerializer(many=True, write_only=True)

    class Meta:
        model = Customer
        fields = ['name', 'dob', 'email', 'wishlist', 'club_points', 'shipping_addresses']

    def update(self, instance, validated_data):
        shipping_addresses_data = validated_data.pop('shipping_addresses', [])

        # Update the Customer instance
        instance.name = validated_data.get('name', instance.name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.email = validated_data.get('email', instance.email)
        instance.wishlist = validated_data.get('wishlist', instance.wishlist)
        instance.club_points = validated_data.get('club_points', instance.club_points)
        instance.save()

        # Update or create ShippingAddress instances
        for address_data in shipping_addresses_data:
            ShippingAddress.objects.update_or_create(
                customer=instance,
                phone_number=address_data.get('phone_number'),
                defaults=address_data
            )

        return instance
