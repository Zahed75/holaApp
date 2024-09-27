from rest_framework import serializers
from products.models import *
from products.serializers import ProductSerializer
from category.models import *




class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    coverImage = serializers.ImageField(required=False)  # Ensure this is allowed

    class Meta:
        model = Category
        fields = ['categoryName', 'id', 'user', 'parentCategory', 'slug', 'products', 'coverImage']
        read_only_fields = ['id', 'slug']

    def get_products(self, obj):
        products = Product.objects.filter(category=obj)
        return ProductSerializer(products, many=True, context=self.context).data

    def get_coverImage(self, obj):
        if obj.coverImage:
            return self.context['request'].build_absolute_uri(obj.coverImage.url)
        return None
