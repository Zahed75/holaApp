from rest_framework import serializers
from .models import Product, ProductImage, Category, Inventory
from django.conf import settings


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'size', 'quantity', 'barCode', 'available']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_type', 'image']

    def get_image(self, obj):
        # Return only the relative URL for the image
        return obj.image.url if obj.image and hasattr(obj.image, 'url') else None


# class ProductSerializer(serializers.ModelSerializer):
#     images = ProductImageSerializer(many=True, required=False)
#     inventory = InventorySerializer(many=True, read_only=True)
#     sizeCharts = serializers.SerializerMethodField()  # Add this field to include sizeCharts
#     featureImage = serializers.SerializerMethodField()  # Add this field to include featureImage
#     is_inventory_available = serializers.SerializerMethodField()  # Add this field to check inventory availability
#
#     class Meta:
#         model = Product
#         fields = [
#             'id', 'productName', 'productDescription', 'seoTitle', 'seoDescription', 'productShortDescription',
#             'color', 'regularPrice', 'salePrice', 'saleStart', 'saleEnd', 'sizeCharts', 'fabric',
#             'weight', 'dimension_length', 'dimension_width', 'dimension_height', 'featureImage',
#             'created', 'updated', 'inventory', 'images', 'is_inventory_available'
#         ]
#
#     def get_sizeCharts(self, obj):
#         return obj.sizeCharts.url if obj.sizeCharts and hasattr(obj.sizeCharts, 'url') else None
#
#     def get_featureImage(self, obj):
#         return obj.featureImage.url if obj.featureImage and hasattr(obj.featureImage, 'url') else None
#
#     def get_is_inventory_available(self, obj):
#         return obj.inventory.exists() if hasattr(obj, 'inventory') and obj.inventory.exists() else False
#


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    inventory = InventorySerializer(many=True, read_only=True)
    sizeCharts = serializers.SerializerMethodField()
    featureImage = serializers.SerializerMethodField()
    is_inventory_available = serializers.SerializerMethodField()

    # Expecting a comma-separated string for colors when writing
    color = serializers.CharField(write_only=True)  # Input as string (e.g., "Red,Pink")
    color_list = serializers.SerializerMethodField()  # For output as a list

    class Meta:
        model = Product
        fields = [
            'id', 'productName', 'productDescription', 'seoTitle', 'seoDescription', 'productShortDescription',
            'color', 'color_list',  # Include both fields for input and output
            'regularPrice', 'salePrice', 'saleStart', 'saleEnd', 'sizeCharts', 'fabric',
            'weight', 'dimension_length', 'dimension_width', 'dimension_height', 'featureImage',
            'created', 'updated', 'inventory', 'images', 'is_inventory_available'
        ]

    def get_color_list(self, obj):
        """Convert the stored color string to a list for response."""
        return obj.color.split(',') if obj.color else []

    # Override to save colors as a comma-separated string during creation
    def create(self, validated_data):
        colors = validated_data.pop('color', '')  # Get the comma-separated string
        validated_data['color'] = colors  # Store as is
        return super().create(validated_data)

    # Override to handle colors as a comma-separated string during update
    def update(self, instance, validated_data):
        colors = validated_data.pop('color', '')  # Get the comma-separated string
        validated_data['color'] = colors  # Store as is
        return super().update(instance, validated_data)

    def get_sizeCharts(self, obj):
        return obj.sizeCharts.url if obj.sizeCharts and hasattr(obj.sizeCharts, 'url') else None

    def get_featureImage(self, obj):
        return obj.featureImage.url if obj.featureImage and hasattr(obj.featureImage, 'url') else None

    def get_is_inventory_available(self, obj):
        return obj.inventory.exists() if hasattr(obj, 'inventory') and obj.inventory.exists() else False

    # Override the create method to store colors correctly
    def create(self, validated_data):
        colors = validated_data.pop('color', '')  # Get the comma-separated string
        validated_data['color'] = colors  # Store as is
        return super().create(validated_data)

    # Override the update method to handle colors correctly
    def update(self, instance, validated_data):
        colors = validated_data.pop('color', '')  # Get the comma-separated string
        validated_data['color'] = colors  # Store as is
        return super().update(instance, validated_data)
