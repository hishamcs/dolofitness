from .models import ProductVariation,Brand,Product
from django.db.models import Max,Min

def get_filters(request):
    brands          = Product.objects.distinct().values('brand__brand_name', 'brand__id')
    flavours        = ProductVariation.objects.distinct().values('flavour')
    weights         = ProductVariation.objects.distinct().values('weight')
    min_max_price   = ProductVariation.objects.aggregate(Min('price'), Max('price'))    
    data   = {
        'brands':brands,
        'flavours':flavours,
        'weights':weights,
        'min_max_price':min_max_price,
    }
    return data