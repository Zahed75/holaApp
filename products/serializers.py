from rest_framework import serializers
from .models import *
from category.models import *
from category.serializers import *




class ProductSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for handling multiple categories
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        # Pop categories from the validated_data since they are handled separately
        categories = validated_data.pop('category', [])
        product = Product.objects.create(**validated_data)
        # Set categories after product creation
        product.category.set(categories)
        return product

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', None)
        if categories is not None:
            instance.category.set(categories)  # Update categories
        return super().update(instance, validated_data)




class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
