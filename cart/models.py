from django.db import models
from account.models import Account
from product.models import ProductVariation

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=50,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user                  = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product_variation     = models.ForeignKey(ProductVariation,on_delete=models.CASCADE)
    cart                  = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity              = models.IntegerField()
    is_active             = models.BooleanField(default=True)
    coupon_code           = models.CharField(max_length=100,blank=True,null=True)
    discount_amount       = models.FloatField(default=0.0)

    def sub_total(self):
        return self.product_variation.price*self.quantity

    def __str__(self):
        return self.product_variation.product.product_name
    
    def cartitem_price(self):
        return (self.sub_total() - self.discount_amount)/self.quantity