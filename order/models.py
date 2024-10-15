# orders/models.py
from django.db import models
from django.contrib.auth.models import User
from customer.models import ShippingAddress
from discount.models import Discount
from products.models import Product
from decimal import Decimal
import random


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('digital_payment', 'Digital Payment'),
    ]

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    order_id = models.CharField(max_length=10, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash_on_delivery')
    shipping_address = models.ForeignKey(ShippingAddress, related_name='orders', on_delete=models.CASCADE)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon_code = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

    # Other methods remain unchanged...

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

    def calculate_totals(self):
        """Calculate total price, inclusive VAT, and grand total."""
        total_price = sum(item.price * item.quantity for item in self.order_items.all())

        # Calculate VAT from the inclusive price
        vat_rate = Decimal(0.05)  # 5% VAT rate
        self.vat = total_price - (total_price / (1 + vat_rate))  # VAT extracted from inclusive total

        # Grand total is just the total price + shipping cost, no additional VAT
        self.total_price = total_price
        self.grand_total = total_price + self.shipping_cost
        self.save()

    def save(self, *args, **kwargs):
        """Override save method to create a unique order ID."""
        if not self.order_id:  # Check if order_id is not set
            self.order_id = self.generate_unique_order_id()
        super().save(*args, **kwargs)

    def generate_unique_order_id(self):
        """Generate a unique order ID in the format 'HLG#XXXXX'."""
        while True:
            random_number = random.randint(10000, 99999)
            order_id = f"HLG#{random_number}"

            # Check if the order_id already exists
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.productName} for Order {self.order.id}'
