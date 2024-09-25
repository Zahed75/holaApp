from rest_framework import serializers
from .models import Product, ProductImage, Category, Inventory







class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_type', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    images = ProductImageSerializer(many=True, required=False)
    sizeCharts = serializers.ImageField(required=False)
    featureImage = serializers.ImageField(required=False)  # Single feature image field

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        images_data = validated_data.pop('images', [])
        feature_image_data = validated_data.pop('featureImage', None)
        size_chart_data = validated_data.pop('sizeCharts', None)

        product = Product.objects.create(**validated_data)

        product.category.set(categories)

        # Handle feature image
        if feature_image_data:
            product.featureImage = feature_image_data
            product.save()

        # Handle gallery images
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        # Handle size chart if provided
        if size_chart_data:
            product.sizeCharts = size_chart_data
            product.save()

        return product

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', None)
        images_data = validated_data.pop('images', None)
        feature_image_data = validated_data.pop('featureImage', None)
        size_chart_data = validated_data.pop('sizeCharts', None)

        if categories is not None:
            instance.category.set(categories)

        # Handle feature image update
        if feature_image_data is not None:
            instance.featureImage = feature_image_data

        # Update gallery images if provided
        if images_data is not None:
            instance.images.all().delete()  # Remove old images
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)

        # Update size chart if provided
        if size_chart_data is not None:
            instance.sizeCharts = size_chart_data

        # Update the instance with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance







class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
