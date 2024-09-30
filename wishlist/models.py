from wishlist.modules import *
from products.models import *
from customer.models import *
# Create your models here.



class Wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlists')  # Ensure this is Customer
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user can only have one wishlist entry per product

    def __str__(self):
        # Fetch the first shipping address of the customer (if it exists)
        phone_number = self.user.shipping_addresses.first().phone_number if self.user.shipping_addresses.exists() else "No Phone Number"
        return f"{self.user.name} - {phone_number} - {self.product.productName}"
