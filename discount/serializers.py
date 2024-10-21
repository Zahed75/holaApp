from rest_framework import serializers
from .models import *
from products.serializers import ProductSerializer
from category.serializers import CategorySerializer
from django.contrib.auth.models import User




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Discount Serializer
class DiscountSerializer(serializers.ModelSerializer):
    included_products = ProductSerializer(many=True, read_only=True)  # Nested product details
    excluded_products = ProductSerializer(many=True, read_only=True)  # Nested product details
    included_categories = CategorySerializer(many=True, read_only=True)  # Nested category details
    excluded_categories = CategorySerializer(many=True, read_only=True)  # Nested category details
    blocked_accounts = UserSerializer(many=True, read_only=True)  # Nested user details for blocked accounts

    class Meta:
        model = Discount
        fields = '__all__'