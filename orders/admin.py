from django.contrib import admin
from .models import Order,Payment,OrderProduct
# Register your models here.
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('order_number','payment','status','user','order_total')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variation', 'quantity', 'product_price', 'ordered', 'status', 'shipped_date', 'out_for_delivery_date', 'delivered_date', 'cancelled_date', 'returned_date')



admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderProduct,OrderProductAdmin)
