from django.contrib import admin
from .models import Product,ProductVariation,ProductImage,Brand
# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name','brand_image','description',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','brand','slug','description','image','is_available','category','created_date','modified_date')

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product','flavour','weight','is_active','price','quantity',)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product','image',)
    

admin.site.register(Brand,BrandAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
admin.site.register(ProductImage,ProductImageAdmin)