from rest_framework import serializers
from .models import Product, ProductImage, Category, Inventory
from django.conf import settings


#
# class ProductImageSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ProductImage
#         fields = ['id', 'image_type', 'image']
#
#     def get_image(self, obj):
#         # Generate absolute URL for the image
#         request = self.context.get('request')
#         return request.build_absolute_uri(obj.image.url) if obj.image else None
#
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
#     images = ProductImageSerializer(many=True, required=False)
#     sizeCharts = serializers.SerializerMethodField()
#     featureImage = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#     def get_sizeCharts(self, obj):
#         request = self.context.get('request')
#         return request.build_absolute_uri(obj.sizeCharts.url) if obj.sizeCharts else None
#
#     def get_featureImage(self, obj):
#         request = self.context.get('request')
#         return request.build_absolute_uri(obj.featureImage.url) if obj.featureImage else None
#





class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_type', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url) if obj.image else None
        else:
            # Use SITE_URL in case request is not available
            return f"{settings.SITE_URL}{obj.image.url}" if obj.image else None

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
        if request:
            return request.build_absolute_uri(obj.sizeCharts.url) if obj.sizeCharts else None
        else:
            return f"{settings.SITE_URL}{obj.sizeCharts.url}" if obj.sizeCharts else None

    def get_featureImage(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.featureImage.url) if obj.featureImage else None
        else:
            return f"{settings.SITE_URL}{obj.featureImage.url}" if obj.featureImage else None








class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
