from django.shortcuts import render,get_object_or_404,HttpResponse
from product.models import Product,ProductVariation,ProductImage
from category.models import Category
from django.db.models import Q
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
def shop(request,category_slug=None):
    category = None
    pro_vars = []
    if category_slug == None:
        # products = Product.objects.all().filter(is_available=True).order_by('id')
        products = Product.objects.all().filter(is_available=True)
        for product in products:
            variations = ProductVariation.objects.filter(product=product, is_active=True).order_by('id')
            for variation in variations:
                pro_vars.append(variation)
        
        
        paginator = Paginator(pro_vars,8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = len(pro_vars)
    else:
        category = get_object_or_404(Category,slug=category_slug)
        products=Product.objects.all().filter(is_available=True,category=category)
        for product in products:
            variations = ProductVariation.objects.filter(product=product,is_active=True).order_by('id')
            for variation in variations:
                pro_vars.append(variation)
        paginator = Paginator(pro_vars,5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = len(pro_vars)
    context = {
        'products':paged_products,
        'products_count':products_count,
        'category':category,
        
    }
    return render(request,'shop/shop.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product      = Product.objects.get(category__slug=category_slug,slug=product_slug,is_available=True)
        product_images      = ProductImage.objects.filter(product=single_product)
        product_variations  = ProductVariation.objects.filter(product=single_product,is_active=True)
        

        unique_flavours     = []
        unique_weights      = []
        for i in product_variations:
            if i.flavour not in unique_flavours:
                unique_flavours.append(i.flavour)
            if i.weight not in unique_weights:
                unique_weights.append(i.weight) 
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'product_images':product_images,
        'product_variations':product_variations,
        'flavours':unique_flavours,
        'weights':unique_weights,
    }
    return render(request,'shop/product_detail.html',context)


def get_weight(request):
    flavour         = request.GET.get('flavour')
    proudct_id      = request.GET.get('product_id')
    product_vars = ProductVariation.objects.filter(product_id=proudct_id,flavour=flavour,is_active=True)
    weights = []
    for i in product_vars:
        weights.append(i.weight)
    response = {
        'weights':weights,
    }
    return JsonResponse(response)

def get_product_details(request):
    weight = request.GET.get('weight')
    flavour = request.GET.get('flavour')
    product_id = request.GET.get('product_id')
    
    product_variation = ProductVariation.objects.get(product_id=product_id,flavour=flavour,weight=weight,is_active=True)
    quantity = product_variation.quantity
    price = product_variation.price
    response = {
        'quantity':quantity,
        'price':price,
    }
    return JsonResponse(response)
    

# search for product

def search(request):
    if 'keyword' in request.GET:
        pro_vars = []
        keyword = request.GET['keyword']
        if keyword:
            
            products = Product.objects.order_by('-id').filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            
            for product in products:
                variations = ProductVariation.objects.filter(product=product, is_active=True)
                for variation in variations:
                    pro_vars.append(variation)
        
        products_count = len(pro_vars)
    context = {
        'products':pro_vars,
        'products_count':products_count,
        'keyword':keyword,
    }
    return render(request, 'shop/shop.html', context)



# filter the product

def filter_product(request):
    
    flavours = request.GET.getlist('flavour[]')
    brands = request.GET.getlist('brand[]')
    weights = request.GET.getlist('weight[]')
    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')
    allproduct_variations = ProductVariation.objects.all().order_by('-id').distinct()

    allproduct_variations = allproduct_variations.filter(price__gte=min_price)
    allproduct_variations = allproduct_variations.filter(price__lte=max_price) 
    
    
    if len(flavours) > 0:
        allproduct_variations = allproduct_variations.filter(flavour__in=flavours).distinct()
    if len(brands) > 0 :
        allproduct_variations = allproduct_variations.filter(product__brand__in=brands).distinct()
    if len(weights) > 0:
        allproduct_variations = allproduct_variations.filter(weight__in=weights).distinct()

    products_count = allproduct_variations.count()
    temp = render_to_string('shop/ajax/product_list.html', {'products':allproduct_variations})
    return JsonResponse({'data':temp,  'products_count':products_count})
