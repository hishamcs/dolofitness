from django.contrib import admin
from .models import Coupon
# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'min_amount', 'discount_amount', 'active')

admin.site.register(Coupon,CouponAdmin)