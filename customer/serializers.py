from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customerInfo', 'email', 'dob']

class ShippingAddressSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()  # Nested Customer serializer

    class Meta:
        model = ShippingAddress
        fields = ['customer', 'phoneNumber', 'address', 'area']
