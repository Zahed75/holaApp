from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    featureImageURL = serializers.SerializerMethodField()
    productsGalleryURL = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'productName', 'regularPrice', 'featureImageURL', 'productsGalleryURL']

    # Get full URL for featureImage
    def get_featureImageURL(self, obj):
        request = self.context.get('request')
        if obj.featureImage:
            return request.build_absolute_uri(obj.featureImage.url)
        return None

    # Get full URL for productsGallery
    def get_productsGalleryURL(self, obj):
        request = self.context.get('request')
        if obj.productsGallery:
            return request.build_absolute_uri(obj.productsGallery.url)
        return None
