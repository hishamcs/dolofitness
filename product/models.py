from django.db import models
from category.models import Category
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Brand(models.Model):
    brand_name      = models.CharField(max_length=60,unique=True)
    brand_image     = models.ImageField(upload_to='photos/brand',blank=True)
    description     = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.brand_name
    
    


class Product(models.Model):
    product_name    = models.CharField(max_length=200,unique=True)
    brand           = models.ForeignKey(Brand, on_delete=models.CASCADE)
    slug            = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    description     = models.TextField(max_length=500,blank=True)
    image           = models.ImageField(upload_to='photos/products',blank=True)
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_deatill',args=[self.category.slug,self.slug,])

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        # Generate slug from category name if not provided
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    image           = models.ImageField(upload_to='photos/products',blank=True)
    

class ProductVariation(models.Model):
    product         = models.ForeignKey(Product,on_delete=models.CASCADE)
    flavour         = models.CharField(max_length=50)
    weight          = models.CharField(max_length=10)
    is_active       = models.BooleanField(default=True)
    price           = models.FloatField()
    quantity        = models.IntegerField()

    class Meta:
        unique_together = ('product', 'flavour','weight')
    
    def __str__(self):
        return self.product.product_name + "--" + self.flavour+" " + str(self.weight)
    

    





    