from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    category_name   = models.CharField(max_length=50,unique=True)
    slug            = models.SlugField(max_length=100,unique=True,null=True,blank=True)
    description     = models.TextField(max_length=255,blank=True)
    category_image  = models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
    def __str__(self):
        return self.category_name
    def save(self, *args, **kwargs):
        # Generate slug from category name if not provided
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)
    