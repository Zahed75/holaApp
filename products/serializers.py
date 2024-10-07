from rest_framework import serializers
from .models import Product, ProductImage, Category, Inventory
from django.conf import settings


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id','size', 'quantity', 'barCode', 'available']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_type', 'image']

    def get_image(self, obj):
        # Return only the relative URL for the image
        return obj.image.url if obj.image and hasattr(obj.image, 'url') else None



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    inventory = InventorySerializer(many=True, read_only=True)
    sizeCharts = serializers.SerializerMethodField()  # Add this field to include sizeCharts
    featureImage = serializers.SerializerMethodField()  # Add this field to include featureImage
    is_inventory_available = serializers.SerializerMethodField()  # Add this field to check inventory availability

    class Meta:
        model = Product
        fields = [
            'id', 'productName', 'productDescription', 'seoTitle', 'seoDescription', 'productShortDescription',
            'color', 'regularPrice', 'salePrice', 'saleStart', 'saleEnd', 'sizeCharts', 'fabric',
            'weight', 'dimension_length', 'dimension_width', 'dimension_height', 'featureImage',
            'created', 'updated', 'inventory', 'images', 'is_inventory_available'
        ]

    def get_sizeCharts(self, obj):
        return obj.sizeCharts.url if obj.sizeCharts and hasattr(obj.sizeCharts, 'url') else None

    def get_featureImage(self, obj):
        return obj.featureImage.url if obj.featureImage and hasattr(obj.featureImage, 'url') else None

    def get_is_inventory_available(self, obj):
        return obj.inventory.exists() if hasattr(obj, 'inventory') and obj.inventory.exists() else False
