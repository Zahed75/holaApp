from rest_framework import serializers
from .models import *
from category.serializers import *


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_type', 'image']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )
    images = ProductImageSerializer(many=True, required=False)
    sizeCharts = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        images_data = validated_data.pop('images', [])

        # Create product instance
        product = Product.objects.create(**validated_data)

        # Set categories
        product.category.set(categories)

        # Save the images
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        return product

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', None)
        images_data = validated_data.pop('images', None)

        if categories is not None:
            instance.category.set(categories)

        # Update images if provided
        if images_data is not None:
            # Remove old images
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)

        return super().update(instance, validated_data)


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
