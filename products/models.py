from category.models import *
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    productName = models.CharField(max_length=322, verbose_name='Product Name')
    productDescription = models.TextField(max_length=10000, verbose_name='Descriptions')
    seoTitle = models.CharField(max_length=400, verbose_name='SEO Title')
    seoDescription = models.TextField(max_length=700)
    productShortDescription = models.TextField(max_length=5000)
    color = models.CharField(max_length=100, verbose_name='Color')


    regularPrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Regular Price')
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sale Price', null=True, blank=True)
    saleStart = models.DateTimeField(verbose_name='Sale Start', null=True, blank=True)
    saleEnd = models.DateTimeField(verbose_name='Sale End', null=True, blank=True)

    # Inventory Section
    sizeCharts = models.ImageField(upload_to='size_charts', null=True, blank=True, verbose_name='Size Charts')
    fabric = models.CharField(max_length=200, verbose_name='Fabric')

    # Shipping Section
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Weight (kg)')
    dimension_length = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Length (cm)')
    dimension_width = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Width (cm)')
    dimension_height = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Height (cm)')
    featureImage = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Feature Image')  # Single feature image
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.productName

    # Check if the product is on sale
    @property
    def on_sale(self):
        current_time = timezone.now()
        return (
            self.salePrice is not None and
            self.salePrice < self.regularPrice and
            (self.saleStart is None or self.saleStart <= current_time) and
            (self.saleEnd is None or self.saleEnd >= current_time)
        )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_type = models.CharField(max_length=20, choices=[('gallery', 'Gallery Image')], default='gallery')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.productName} - {self.image_type}"


class Inventory(models.Model):
    product = models.ForeignKey(Product, related_name='inventory', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, verbose_name='Size')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    barCode = models.CharField(max_length=100, unique=True, verbose_name='Bar Code')
    available = models.BooleanField(default=True, verbose_name='Available')

    def __str__(self):
        return f'{self.product.productName} - {self.size}'



