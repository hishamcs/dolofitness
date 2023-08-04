from django.core.serializers import serialize
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import JsonResponse
from orders.models import Order,Payment,OrderProduct
from account.models import UserAddress,Wallet
from django.contrib import messages
from product.models import ProductVariation
from cart.models import CartItem
from offers.models import Coupon
import datetime
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

    






@login_required(login_url='user_login')
def order_details(request):
    order_number = request.GET.get('order_number')
    order = get_object_or_404(Order, order_number=order_number)
    if order.coupon is None:
        discount = 0
    else:
        discount = order.coupon.discount_amount
    ordered_products = OrderProduct.objects.filter(order=order)
    order_details ={
        'order_number':order.order_number,
        'transaction_id':order.payment.payment_id,
        'order_date':order.order_date.strftime("%d %B %Y"),
        'status':order.payment.status,
        'fullname':order.address.full_name(),
        'full_address':order.address.full_address(),
        'city':order.address.city,
        'state':order.address.state,
        'country':order.address.country,
        'postcode':order.address.postcode,
        'tax':order.tax,
        'order_total':order.order_total,
        'subtotal':order.order_total-order.tax,
        'discount':discount,
        'ordered_products':[
            {
                'product_name':orderproduct.product_variation.product.product_name,
                'flavour':orderproduct.product_variation.flavour,
                'weight' :orderproduct.product_variation.weight,
                'quantity':orderproduct.quantity,
                'product_price':orderproduct.product_price,
                'total':orderproduct.quantity * orderproduct.product_price,
            }
            for orderproduct in ordered_products
        ]
    
    }
    return JsonResponse(order_details)




    
@login_required(login_url='user_login')
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number)
        orderproducts = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        discount = order.coupon
        if discount is None:
            discount = 0
        else:
            discount = order.coupon.discount_amount
        
        
        subtotal = 0
        for i in orderproducts:
            subtotal += i.product_price * i.quantity
        subtotal = subtotal + discount

        context = {
            'order': order,
            'discount':discount,
            'ordered_products': orderproducts,
            'order_number': order_number,
            'transID': transID,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render(request,'orders/order_complete.html',context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('index')
    

@login_required(login_url='user_login')
def order_act(request):
    
    orderproduct_id = request.POST.get('orderproduct_id')
    orderproduct = OrderProduct.objects.get(order__user=request.user,id=orderproduct_id)
    product_variation = orderproduct.product_variation
    order = orderproduct.order
    order.order_total -= orderproduct.total()
    orderproduct.status = 'Cancelled'
    payment_method = orderproduct.order.payment.payment_method
    if payment_method != 'Cash On Delivery':
        wallet = Wallet.objects.get(user_id=orderproduct.order.user.id)
        wallet.balance += orderproduct.total()
        wallet.save()
    # orderproduct.product_price = 0
    product_variation.quantity += orderproduct.quantity
    
    product_variation.save()
    orderproduct.save()
    order.save()
    return JsonResponse({'message':'hi'})



# place order 
@login_required(login_url='user_login')
def place_order(request, total=0, quantity=0):

    address_id = request.POST.get('address_radio')
    payment_method = request.POST.get('payment_method')
    current_user = request.user
    cart_items = CartItem.objects.all().filter(user=current_user)

    coupon_code = cart_items[0].coupon_code
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')
    
    # grand_total = 0
    tax = 0
    discount = 0
    for cart_item in cart_items:
        total += cart_item.sub_total()
        quantity += cart_item.quantity
        discount += cart_item.discount_amount

    # discount = round(discount)
    grand_total = total + tax - discount
    addresses = UserAddress.objects.filter(user=current_user)

    if len(addresses) == 0:
        messages.warning(request, 'Please add an address for checkout...!')   
        return redirect('my_address')
    address = UserAddress.objects.get(user=current_user, pk=address_id)

    context = {
        'address':address,
        'cart_items':cart_items,
        'discount':discount,
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
        'payment_method':payment_method,
    }
    return render(request, 'orders/payment_test2.html', context)


# payments test
@login_required(login_url='user_login')
def payments(request):
    
    body = json.loads(request.body)
    payment_id = body['transID']
    payment_method = body['payment_method']

    address_id = body['address_id']
    current_user = request.user
    cart_items = CartItem.objects.all().filter(user=current_user)
    cart_count = cart_items.count()
    coupon_code = cart_items[0].coupon_code
    coupon = Coupon.objects.filter(code=coupon_code)

    if coupon.count() == 0:
        coupon =None
    else:
        coupon = Coupon.objects.get(code=coupon_code)
        
    
    address = UserAddress.objects.get(user=current_user, pk=address_id)
    
    
    grand_total = 0
    tax =0
    discount =0
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += cart_item.sub_total()
        quantity += cart_item.quantity
        discount += cart_item.discount_amount
    
    

    grand_total = total + tax - round(discount)      # new updation for rounding coupon discount
    


    if payment_method == 'Wallet':                      # wallet updation
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance -= grand_total
        wallet.save()

    payment = Payment(
        user = current_user,
        payment_id = payment_id,
        payment_method = payment_method,
        amount_paid = grand_total,
        status = body['status']
    )
    payment.save()


    data                      = Order()
    data.user                 = current_user
    data.address              = address
    data.order_total          = grand_total
    data.tax                  = tax
    data.ip                   = request.META.get('REMOTE_ADDR') 
    data.coupon               = coupon
    data.payment              = payment
    data.save()
    yr  = int(datetime.date.today().strftime('%Y'))
    dt  = int(datetime.date.today().strftime('%d'))
    mt  = int(datetime.date.today().strftime('%m'))
    d   = datetime.date(yr, mt, dt)
    current_date = d.strftime("%Y%m%d")
    order_number = current_date + str(data.id)
    data.order_number = order_number
    data.save()

    for cart_item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = data.id
        orderproduct.product_variation_id = cart_item.product_variation.id
        orderproduct.quantity = cart_item.quantity
        orderproduct.product_price = cart_item.cartitem_price()
        orderproduct.ordered = True
        orderproduct.save()
        
        product_variation = ProductVariation.objects.get(id=cart_item.product_variation_id)
        product_variation.quantity -= cart_item.quantity
        product_variation.save()

    CartItem.objects.filter(user=current_user).delete()



    data = {
        'order_number': data.order_number,
        'transID': payment.payment_id
    }

    return JsonResponse(data)



@login_required(login_url='user_login')
def order_return(request):
    orderproduct_id = request.POST.get('orderproduct_id')
    orderproduct = OrderProduct.objects.get(order__user=request.user, id=orderproduct_id)
    orderproduct.status = 'Return Requested'
    orderproduct.save()
    return JsonResponse({'message':'The return for the product has been requested...'})






