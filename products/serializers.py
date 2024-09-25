from rest_framework import serializers
from .models import Product, ProductImage, Category, Inventory






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
    sizeCharts = serializers.ImageField(required=False)  # Change to handle a single image file

    class Meta:
        model = Product
        fields = '__all__'  # This includes the sizeCharts field

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        images_data = validated_data.pop('images', [])
        size_chart_data = validated_data.pop('sizeCharts', None)  # Now single image

        # Create product instance
        product = Product.objects.create(**validated_data)

        # Set categories
        product.category.set(categories)

        # Save the images
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        # Save the size chart if provided
        if size_chart_data:
            product.sizeCharts = size_chart_data
            product.save()

        return product

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', None)
        images_data = validated_data.pop('images', None)
        size_chart_data = validated_data.pop('sizeCharts', None)

        if categories is not None:
            instance.category.set(categories)

        # Update images if provided
        if images_data is not None:
            # Remove old images
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)

        # Update size chart if provided
        if size_chart_data is not None:
            instance.sizeCharts = size_chart_data

        # Update instance with remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
