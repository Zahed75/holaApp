from django.db import models
from customer.models import Customer
from products.models import Product

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.name} - {self.product.productName} (Qty: {self.quantity})'

    # Calculate the total price of the cart item (based on sale price if on sale)
    @property
    def total_price(self):
        if self.product.on_sale:
            return self.product.salePrice * self.quantity
        return self.product.regularPrice * self.quantity
