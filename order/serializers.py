from rest_framework import serializers
from .models import *
from auths.models import *



class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    customerPhoneNumber = serializers.CharField(read_only=True)
    customerName = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['orderId', 'customer', 'customerName', 'customerPhoneNumber', 'orderTime', 'amount', 'origin',
                  'orderStatus', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        user_profile = UserProfile.objects.get(user=request.user)

        # Automatically fill in customer details
        validated_data['customer'] = user_profile
        validated_data['customerPhoneNumber'] = user_profile.phone_number
        validated_data['customerName'] = user_profile.user.username  # Assuming username is the customer's name

        return super().create(validated_data)
