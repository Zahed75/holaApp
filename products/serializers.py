from rest_framework import serializers
from .models import Product, ProductImage, Category, Inventory
from django.conf import settings



class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_type', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if obj.image and hasattr(obj.image, 'url') else None



class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    images = ProductImageSerializer(many=True, required=False)
    sizeCharts = serializers.SerializerMethodField()
    featureImage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_sizeCharts(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.sizeCharts.url) if obj.sizeCharts and hasattr(obj.sizeCharts, 'url') else None

    def get_featureImage(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.featureImage.url) if obj.featureImage and hasattr(obj.featureImage, 'url') else None





class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
