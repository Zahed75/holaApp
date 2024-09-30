from wishlist.modules import *
# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user can only have one wishlist entry per product

    def __str__(self):
        return f"{self.user.phone_number} - {self.product.productName}"
