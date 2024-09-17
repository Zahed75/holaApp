from rest_framework import serializers
from .models import *


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'phone_number', 'address', 'area']

class CustomerSerializer(serializers.ModelSerializer):
    shipping_addresses = ShippingAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['name', 'dob', 'email', 'wishlist', 'club_points', 'shipping_addresses']
