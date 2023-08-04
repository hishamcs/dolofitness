from django.shortcuts import render,redirect,HttpResponse
from product.models import Product,ProductImage,ProductVariation,Brand
from category.models import Category
from category.forms import CategoryForm
from account.models import Account,Wallet
from offers.models import Coupon
from orders.models import Order,OrderProduct
from django.http import JsonResponse
from product.forms import ProductForm,ProductVariationForm,BrandForm
from offers.models import Coupon
from offers.forms import CouponForm
from django.core.paginator import Paginator
from django.db.models import Count,Sum,Q
from django.utils import timezone
from datetime import datetime,timedelta,date
import datetime
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
# Create your views here.
@never_cache
def admin_login(request):
    if request.user.is_superuser:
        return redirect('admin_home')
    if request.method == "POST":
        print('request POST :', request.POST)
        email = request.POST.get('email')
        passw = request.POST.get('password')
        user = authenticate(email=email,password=passw)
        print('user : ',user)
        if user is not None and user.is_superuser:
           login(request, user)
           return redirect('admin_home') 
        else:
            messages.error(request, 'Invalid credentails...')
    return render(request, 'admn/admin_login.html')


@never_cache
def admin_home(request):
    if request.user.is_superuser:
        user_count = Account.objects.filter(is_superuser=False).count()
        delivered_products = OrderProduct.objects.all().filter(status='Delivered')
        revenue = sum(product.total() for product in delivered_products)
        total_orders = OrderProduct.objects.all().count()
        status_counts = OrderProduct.objects.values('status').annotate(count=Count('status'))
        product_count = Product.objects.all().count()
        category_count = Category.objects.all().count()
        current_year = timezone.now().year
        order_detail = OrderProduct.objects
        monthly_order_count = []
        month = timezone.now().month
        order_detail = OrderProduct.objects.filter(
            order__order_date__lt=date(current_year, 12, 31),
            status='Delivered',
        )

        for i in range(1, month + 1):
            monthly_order = order_detail.filter(order__order_date__month=i).count()
            monthly_order_count.append(monthly_order)


        today = datetime.datetime.now()
        neworders = OrderProduct.objects.filter(order__order_date__month=today.month).values('order__order_date__date').annotate(orderitemscount=Count('id', filter=Q(status='Order Placed')))
        cancelledorders = OrderProduct.objects.filter(order__order_date__month=today.month).values('order__order_date__date').annotate(cancelleditemscount=Count('id',filter=Q(status='Cancelled')))
        returnorders = OrderProduct.objects.filter(order__order_date__month=today.month).values('order__order_date__date').annotate(returnedorderscount=Count('id', filter=Q(status='Returned')))
        deliveredorders = OrderProduct.objects.filter(order__order_date__month=today.month).values('order__order_date__date').annotate(delivereditemscount=Count('id', filter=Q(status='Delivered')))

        orderitems = OrderProduct.objects.filter(status='Delivered')
        last_date = datetime.datetime.now().date()
        first_date = last_date - timedelta(days=6)
        amount_per_day = []
        date_list = []
        for i in range(1,8):
            total_amount_per_day = 0
            for order in orderitems:
                if order.order.order_date.date() == first_date:
                    total_amount_per_day += order.total()
            amount_per_day.append(total_amount_per_day)
            date_list.append(first_date)
            first_date = first_date + timedelta(days=1)
    
  
        context = {
            'revenue':revenue,
            'total_orders':total_orders,
            'status_counts':status_counts,
            'product_count':product_count,
            'category_count':category_count,
            'user_count':user_count,
            'amount_per_day':amount_per_day,
            'date_list':date_list,
            'neworders':neworders,
            'cancelledorders':cancelledorders,
            'returnorders':returnorders,
            'deliveredorders':deliveredorders,
            'monthly_order_count':monthly_order_count,

        }
        return render(request,'admn/ad_home.html', context)
    return redirect('admin_login')

@login_required(login_url='admin_login')
@never_cache
def ad_categories(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }
    return render(request, 'admn/category.html', context)

@login_required(login_url='admin_login')
@never_cache
def ad_products(request):
    products = Product.objects.all()
    context = {
        'products':products,
    }
    return render(request, 'admn/products.html', context)


@login_required(login_url='admin_login')
@never_cache
def ad_products_variations(request, product_id=0):
    if product_id == 0:
        product_variations = ProductVariation.objects.all()
        context = {
            'product_variations':product_variations,
        }
        return render(request, 'admn/product_variations.html',context)
    else:
        product_variations = ProductVariation.objects.all().filter(product__id=product_id)
        context = {
            'product_variations':product_variations,
        }
        return render(request, 'admn/product_variations.html',context)
        

@login_required(login_url='admin_login')
@never_cache
def ad_brand(request):
    brands = Brand.objects.all()
    context = {
        'brands':brands,
    }
    return render(request, 'admn/brand.html', context)

@login_required(login_url='admin_login')
@never_cache
def ad_users(request):
    users = Account.objects.all()
    context = {
        'users':users,
    }
    return render(request, 'admn/users.html', context)

@login_required(login_url='admin_login')
@never_cache
def ad_coupons(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons':coupons,
    }
    return render(request, 'admn/coupon.html', context)

@login_required(login_url='admin_login')
@never_cache
def ad_orders(request):
    orders = Order.objects.all().order_by('-id')
    context = {
        'orders':orders,
    }
    return render(request, 'admn/order.html', context)

@login_required(login_url='admin_login')
@never_cache
def order_details(request, order_num):
    order = Order.objects.get(order_number=order_num)
    order_items = OrderProduct.objects.filter(order__order_number=order_num)
    context = {
        'order_items':order_items,
        'order':order,
    }
    return render(request, 'admn/order_details.html', context)


@login_required(login_url='admin_login')
@never_cache
def ad_edit_category(request,category_id=0):
    if category_id == 0:
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('ad_categories')
        
        form = CategoryForm()
    else:
        category = Category.objects.get(id=category_id)
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES, instance=category) 
            if form.is_valid():
                form.save()
                return redirect('ad_categories')
        form = CategoryForm(instance=category)


    context = {
        'form':form,
    }
    return render(request, 'admn/ad_edit_categry.html', context)

@login_required(login_url='admin_login')
@never_cache
def del_category(request):
    category_id = request.POST.get('category_id')
    category = Category.objects.get(id=category_id)
    category.delete()
    return JsonResponse({'message':'Category deleted successfully'})

@login_required(login_url='admin_login')
@never_cache
def ad_edit_product(request, product_id=0):
    if product_id == 0:
        if request.method == 'POST':
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                product = form.save()
                if request.FILES.get('pr_images') != 0:
                    images = request.FILES.getlist('pr_images')
                    for img in images:
                        image = ProductImage.objects.create(product=product, image=img)
                        image.save()
                return redirect('ad_products')
            else:
                print('form not valid')
                print(form.errors)
        
        form = ProductForm()
    else:
        product = Product.objects.get(id=product_id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('ad_products')
        form = ProductForm(instance=product)
    context = {
        'form':form,
    }
    return render(request, 'admn/ad_edit_product.html', context)
    
@login_required(login_url='admin_login')
@never_cache
def del_product(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    product.delete()
    return JsonResponse({'message':'Product successfully deleted...'})

@login_required(login_url='admin_login')
@never_cache
def deact_product(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    if product.is_available:
        product.is_available = False
        product.save()
        return JsonResponse({'title':'Deactivated','message':'Product deactivated...',})
    else:
        product.is_available = True
        product.save()
        return JsonResponse({'title':'Activated','message':'Product Activated...',})
    

@login_required(login_url='admin_login')
@never_cache
def ad_edit_product_variations(request, product_var_id=0):
    if product_var_id == 0:
        if request.method == 'POST':
            form = ProductVariationForm(request.POST)
            if form.is_valid():
                print('form is valid')
                form.save()
                return redirect('ad_products_variations')
        form = ProductVariationForm()
    else:
        product_variation = ProductVariation.objects.get(id=product_var_id)
        if request.method == "POST":
            form = ProductVariationForm(request.POST, instance=product_variation)
            if form.is_valid():
                form.save()
                return redirect('ad_products_variations')
            else:
                print('form is not valid..')
        form = ProductVariationForm(instance=product_variation)
    context = {
        'form':form,
    }
    return render(request, 'admn/ad_edit_product_variations.html', context)


@login_required(login_url='admin_login')
@never_cache
def ad_del_product_variations(request):
    
    product_variation_id = request.POST.get('product_var_id')
    product_variation = ProductVariation.objects.get(id=product_variation_id)
    product_variation.delete()
    return JsonResponse({'message':'Variation Deleted successfully..'})

@login_required(login_url='admin_login')
@never_cache
def ad_deact_product_variations(request):
    product_var_id = request.POST.get('product_var_id')
    product_variation = ProductVariation.objects.get(id=product_var_id)
    print('print product variation : ', product_variation)
    if product_variation.is_active:
        product_variation.is_active = False
        product_variation.save()
        return JsonResponse({'title':'Deactivatd','message':'Variation deactivated...'})
    else:
        product_variation.is_active = True
        product_variation.save()
        return JsonResponse({'title':'Activated','message':'Variation activated...'})
    
@login_required(login_url='admin_login')
@never_cache
def ad_add_brand(request,brand_id=0):
    if brand_id == 0:
        if request.method == 'POST':
            form = BrandForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('ad_brand')
        form = BrandForm()
    else:
        brand = Brand.objects.get(id=brand_id)
        form =BrandForm(instance=brand)
        if request.method == 'POST':
            form = BrandForm(request.POST, request.FILES, instance=brand)
            if form.is_valid():
                form.save()
                return redirect('ad_brand')
    context = {
        'form':form,
    }
    return render(request, 'admn/ad_add_brand.html', context)

@login_required(login_url='admin_login')
@never_cache
def ad_del_brand(request):
    brand_id = request.POST.get('brand_id')
    brand = Brand.objects.get(id=brand_id)
    brand.delete()
    return JsonResponse({'message':'Brand deleted successfully...'})


@login_required(login_url='admin_login')
@never_cache
def ad_add_coupon(request, coupon_id=0):
    if coupon_id == 0:
        if request.method == "POST":
            form = CouponForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('ad_coupons')
        form = CouponForm()
    else:
        coupon = Coupon.objects.get(id=coupon_id)
        if request.method == 'POST':
            form = CouponForm(request.POST, instance=coupon)
            if form.is_valid():
                form.save()
                return redirect('ad_coupons')
        form = CouponForm(instance=coupon)
    context = {
        'form':form,
    }
    return render(request, 'admn/ad_add_coupon.html', context)

@login_required(login_url='admin_login')
@never_cache
def del_coupon(request):
    print('del coupon is workinggg')
    coupon_id = request.POST.get('coupon_id')
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return JsonResponse({'message':'Coupon deleted successfully...'})




@login_required(login_url='admin_login')
@never_cache
def status_update(request):
    if request.method == "GET":
        orderproduct_id = request.GET['orderproduct_id']
        status = request.GET['status']
        
        orderproduct = OrderProduct.objects.get(id=orderproduct_id)
        if orderproduct.status == 'Return Requested':
            product_variation = orderproduct.product_variation
            order = orderproduct.order
            order.order_total -= orderproduct.total()
            orderproduct.status = 'Returned'

            wallet = Wallet.objects.get(user_id=orderproduct.order.user.id)
            wallet.balance += orderproduct.total()
            wallet.save()
            
            product_variation.quantity += orderproduct.quantity
            product_variation.save()
            order.save()
            status = 'Returned'

        print('status : ', status)
        orderproduct.status = status
        orderproduct.save()
    return JsonResponse({'message':'Status has been changed..'})

@login_required(login_url='admin_login')
@never_cache
def orderitems_active(request):
    exclude_list = [
        'Delivered',
        'Cancelled',
        'Returned',
    ]
    active_orders = OrderProduct.objects.all().exclude(
        status__in=exclude_list
    )
    print('active orders : ',active_orders)
    # paginator = Paginator(active_orders,5)
    # page = request.GET.get('page')
    # paged_products = paginator.get_page(page)

    context = {
        'active_orders':active_orders,
    }
    return render(request,'admn/orderitem_active.html',context)

@login_required(login_url='admin_login')
@never_cache
def orderitems_history(request):
    excluded_list = [
        'Order Placed',
        'Shipped',
        'Out For Delivery',
        'Return Requested'
    ]

    orders = OrderProduct.objects.all().exclude(
        status__in=excluded_list
    ).order_by('-id')
    # paginator = Paginator(orders, 5)
    # page = request.GET.get('page')
    # paged_products = paginator.get_page(page)

    context = {
        'orders':orders,
    }
    return render(request, 'admn/orderitems_history.html', context)



@login_required(login_url='admin_login')
@never_cache
def sales_report(request):
    orders = OrderProduct.objects.all()
    msg = 'nothing'
    if request.method == 'POST':
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        if start_date == end_date:
            orders = OrderProduct.objects.all().filter(order__order_date__date=start_date)
            msg = 'Showing the results of the date : '+ start_date
            
        else:
            orders = OrderProduct.objects.all().filter(order__order_date__range=[start_date,end_date])
            msg = 'Showing the results between '+ start_date + '--' + end_date


    context = {
        'orders':orders,
        'msg':msg,
    }
    return render(request, 'admn/sales_report.html', context)

@login_required(login_url='admin_login')
@never_cache
def yearly_sales(request):
    if request.method == 'POST':
        print('request.post ',request.POST)
        year = request.POST.get('selectedYear')
        print('year : ',year)
        orders = OrderProduct.objects.all().filter(order__order_date__year=year)
        if orders.count() == 0:
            msg = 'No result found for ' + year
        else:
            msg = 'The details of sales in ' + year + ' are :'
        context = {
            'msg':msg,
            'orders':orders,
        }
    return render(request, 'admn/sales_report.html', context)

@login_required(login_url='admin_login')
@never_cache
def monthly_sales(request):
    print('request.post : ', request.POST)
    month = request.POST.get('month')
    orders = OrderProduct.objects.all().filter(order__order_date__month=month)
    if orders.count() == 0:
        msg = 'No result found for this month'
    else:
        msg = 'The details of the sales in this month are : '
    context = {
        'msg':msg,
        'orders':orders,
    }
    return render(request, 'admn/sales_report.html', context)

@login_required(login_url='admin_login')
@never_cache
def deact_coupon(request):
    coupon_id = request.POST.get('coupon_id')
    coupon = Coupon.objects.get(id=coupon_id)
    if coupon.active:
        coupon.active = False
        coupon.save()
        return JsonResponse({'title':'Deactivated', 'message':'coupon deactivated...'})
    else:
        coupon.active = True
        coupon.save()
        return JsonResponse({'title':'Activated','message':'coupon activated...'})

@login_required(login_url='admin_login')
@never_cache       
def deact_user(request):
    user_id = request.POST.get('user_id')
    user = Account.objects.get(id=user_id)
    if user.is_blocked:
        user.is_blocked = False
        user.save()
        return JsonResponse({'title':'Activated','message':'user is now active...'})
    else:
        user.is_blocked = True
        user.save()
        return JsonResponse({'title':'Deactivated', 'message':'user is now deactivated...'})
    

@login_required(login_url='admin_login')
@never_cache
def ad_logout(reuqest):
    logout(reuqest)
    return redirect('admin_login')

