from django.db import models
from account.models import Account
from product.models import ProductVariation
# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product_variation)
    