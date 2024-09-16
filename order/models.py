from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import *
from discount.models import *
from decimal import Decimal



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    customerName=models.CharField(max_length=120, blank=True),
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        # Calculate the total price based on products and discount
        total = sum([item.product.regularPrice * item.quantity for item in self.order_items.all()])

        if self.discount:
            total -= self.discount.coupon_amount

        self.total_price = total
        self.vat = total * Decimal(0.05)  # 5% VAT
        self.grand_total = self.total_price + self.shipping_cost + self.vat
        self.save()

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.productName} - {self.quantity} pcs'
