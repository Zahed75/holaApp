# orders/models.py
from django.db import models
from django.contrib.auth.models import User
from customer.models import ShippingAddress
from discount.models import Discount
from products.models import Product
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.ForeignKey(ShippingAddress, related_name='orders', on_delete=models.CASCADE)  # Ensure this matches
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon_code = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)  # Ensure this is correct

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

    def calculate_totals(self):
        """Calculate total price, VAT, and grand total based on order items."""
        total_price = sum(item.price * item.quantity for item in self.order_items.all())
        self.total_price = total_price
        self.vat = total_price * Decimal(0.05)  # Assuming a 5% VAT rate
        self.grand_total = total_price + self.shipping_cost + self.vat
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.productName} for Order {self.order.id}'
