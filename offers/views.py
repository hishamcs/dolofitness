from django.shortcuts import render
from cart.models import Cart,CartItem
from django.http import JsonResponse
from .models import Coupon
from datetime import datetime
from django.db.models import Q
# Create your views here.

def coupon_verify(request):
    code = request.POST.get('Coupon').upper()
    cart_items = CartItem.objects.filter(user=request.user)
    now = datetime.now()
    
    total_amount = 0
    try:
        coupon = Coupon.objects.get(code=code)
    
    except:
        coupon = None
    
    for cart_item in cart_items:
        total_amount += cart_item.sub_total()


    if(coupon == None):
        return JsonResponse({'message':"Coupon doesn't exist "})
    else:
        if total_amount < coupon.min_amount:
            lack_amount = coupon.min_amount - total_amount
            return JsonResponse({'message':'Please Purchase ₹'+ str(lack_amount) + ' to apply this coupon'})
        
        elif now.date() < coupon.valid_from.date() or now.date() > coupon.valid_to.date():
            return JsonResponse({'message':'Coupon Expired'})
        
        else:
            new_total = total_amount - coupon.discount_amount
            discount_amount = coupon.discount_amount/cart_items.count()
            return JsonResponse({'total_amount':total_amount, 'discount_amount_foreach':discount_amount, 'new_total_amount':new_total, 'coupon_discount':coupon.discount_amount,'coupon_id':coupon.id, 'message':'Coupon has been Applied' })
    
