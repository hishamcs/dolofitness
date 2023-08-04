from django.db import models
from account.models import Account,UserAddress
from product.models import ProductVariation
from offers.models import Coupon
from django.utils import timezone
import datetime
# Create your models here.
class Payment(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id      = models.CharField(max_length=100)
    payment_method  = models.CharField(max_length=100)
    amount_paid     = models.CharField(max_length=100)
    status          = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


    


class Order(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    address         = models.ForeignKey(UserAddress,on_delete=models.CASCADE)
    coupon          = models.ForeignKey(Coupon,on_delete=models.CASCADE,blank=True, null=True)

    order_number    = models.CharField(max_length=20)
    order_date      = models.DateTimeField(auto_now_add=True)
    tax             = models.FloatField()
    order_total     = models.FloatField()
    ip              = models.CharField(blank=True, max_length=20)


    def __str__(self):
        return self.order_number
    
    def discount_amount(self):
        if self.coupon == None:
            return 0
        else:
            return self.coupon.discount_amount

    def order_total_amount(self):
        if self.coupon == None:
            return self.order_total
        else:
            return self.order_total + self.coupon.discount_amount
        

choices = (
    ('Order Placed', 'Order Placed'),
    ('Shipped', 'Shipped'),
    ('Out For Delivery', 'Out For Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)


class OrderProduct (models.Model):
    order                   = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_variation       = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity                = models.IntegerField()
    product_price           = models.FloatField()
    ordered                 = models.BooleanField(default=False)
    updated_at              = models.DateTimeField(auto_now=True)
    status                  = models.CharField(max_length=100,choices=choices,default='Order Placed')
    shipped_date            = models.DateTimeField(blank=True, null=True)
    out_for_delivery_date   = models.DateTimeField(blank=True, null=True)
    delivered_date          = models.DateTimeField(blank=True, null=True)
    cancelled_date          = models.DateTimeField(blank=True, null=True)
    returned_date           = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # print('save is workinggg....')
        if self.status == 'Shipped':
            self.shipped_date = datetime.datetime.now(tz=timezone.utc)
        if self.status == 'Out For Delivery':
            self.out_for_delivery_date = datetime.datetime.now(tz=timezone.utc)
        if self.status == 'Delivered':
            self.delivered_date = datetime.datetime.now(tz=timezone.utc)
        if self.status == 'Cancelled':
            self.cancelled_date = datetime.datetime.now(tz=timezone.utc)
        if self.status == 'Returned':
            self.returned_date = datetime.datetime.now(tz=timezone.utc)
        super(OrderProduct, self).save(*args, **kwargs)


    def __str__(self):
        return self.product_variation.product.product_name
    
    def total(self):
        return self.product_price * self.quantity
