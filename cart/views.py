from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from product.models import ProductVariation
from cart.models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from account.models import UserAddress,Wallet
from account.forms import AddressForm
from offers.models import Coupon
from shop.models import Wishlist
from django.http import JsonResponse


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
    return cart






def cart(request,total=0):
    cart_items = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart        = Cart.objects.get(cart_id=_cart_id(request))
            cart_items  = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total = total + cart_item.sub_total()
    except Cart.DoesNotExist:
        pass
    context = {
        'cart_items':cart_items,
        'total':total,
    }
    return render(request,'shop/cart.html',context)

def add_cart(request,product_id):
    

    current_user = request.user
    flavour = request.POST.get('flavour_pro')
    weight  = request.POST.get('weight_pro')
    product_variation = get_object_or_404(ProductVariation,product_id=product_id,flavour=flavour,weight=weight)
    
    if current_user.is_authenticated:
        if request.method == 'POST':
            is_cart_item_exists = CartItem.objects.filter(product_variation=product_variation,user=current_user).exists()
            if is_cart_item_exists:
                pass
                # cart_item = CartItem.objects.get(product_variation=product_variation, user=current_user)
                # cart_item.quantity += 1
                # cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product_variation = product_variation,
                    quantity = 1,
                    user = current_user,
                )
                cart_item.save()
        return redirect('cart')

    else:
        if request.method == 'POST':
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
            is_cart_item_exists = CartItem.objects.filter(product_variation=product_variation,cart=cart).exists()
            if is_cart_item_exists:
                pass
                # cart_item = CartItem.objects.get(product_variation=product_variation,cart=cart)
                # cart_item.quantity += 1
                # cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product_variation=product_variation,
                    quantity=1,
                    cart=cart,
                )
                cart_item.save()

            

    return redirect('cart')



def remove_cart_item(request,product_variation_id,cart_item_id):
    product_variation = ProductVariation.objects.get(id=product_variation_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product_variation=product_variation, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product_variation=product_variation,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def remove_cart(request,product_variation_id,cart_item_id):
    product_variation = ProductVariation.objects.get(id=product_variation_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product_variation=product_variation,id=cart_item_id,user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product_variation=product_variation,id=cart_item_id,cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')








@login_required(login_url='user_login')
def checkout(request,total=0,coupon_id=0):
    try:
        cart_items  = CartItem.objects.filter(user=request.user,is_active=True)
        if cart_items.count() <=0:
            return redirect('shop')
        
        for cart_item in cart_items:
                total = total+cart_item.sub_total() 
        if coupon_id != 0:
            coupon = Coupon.objects.get(id=coupon_id)
            coupon_discount = coupon.discount_amount
            total_afdiscount = total - coupon.discount_amount
            discount_per_item = round(coupon.discount_amount/cart_items.count(),1)
            
            for cart_item in cart_items:
                cart_item.coupon_code = coupon.code
                cart_item.discount_amount = discount_per_item
                cart_item.save()
        else:
            coupon_discount = 0
            total_afdiscount = total-coupon_discount
            for cart_item in cart_items:
                cart_item.coupon_code = None
                cart_item.discount_amount=0.0
                cart_item.save()

    except ObjectDoesNotExist:
        pass

    addresses = UserAddress.objects.all().filter(user=request.user)
    try:
        default_address = UserAddress.objects.get(user=request.user, default_addr=True)
    except UserAddress.DoesNotExist:
        default_address = None
    wallet_amount = Wallet.objects.get(user_id=request.user.id).balance
    form = AddressForm()
    context = {
        'cart_items':cart_items,
        'total':total,
        'coupon_discount':coupon_discount,
        'total_afdiscount':total_afdiscount,
        'addresses':addresses,
        'default_address':default_address,
        'form':form,
        'wallet_amount':wallet_amount,
        }
    return render(request,'shop/checkout.html',context)


@login_required(login_url='user_login')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    cart_items = CartItem.objects.filter(user=request.user)
    variations = cart_items.values_list('product_variation', flat=True).distinct()
    print('variations : ', variations)
    
    context = {
        'wishlist':wishlist,
        'cart_items':cart_items,
        'variations':variations,
    }
    return render(request, 'shop/wishlist.html', context)


def add_to_wishlist(request):
    current_user = request.user
    flavour = request.POST.get('flavour')
    weight  = request.POST.get('weight')
    product_id = request.POST.get('product_id')
    
    
    product_variation = get_object_or_404(ProductVariation, flavour=flavour, weight=weight, product__id=product_id)
    if request.method == "POST":
        is_wishlist_exists = Wishlist.objects.filter(product_variation=product_variation, user=current_user).exists()
        if is_wishlist_exists:
            return JsonResponse({'message':'Item already in the Wishlist...'})
        else:
            
            wishlist = Wishlist.objects.create(
                product_variation=product_variation,
                user=current_user,
            )
            wishlist.save()
            return JsonResponse({'message':'Product successfully added to wishlist'})
    return JsonResponse({'message':'success'})

# Delete wishlist item

def del_wishlist_item(request):
    wishlist_item_id = request.POST.get('wishlist_item_id')
    item = Wishlist.objects.get(id=wishlist_item_id)
    item.delete()
    return JsonResponse({'message':'item deleted from wishlist...'})



# increment quantity of cart item
def increment_qty(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)

        if cart_item.quantity + 1 > cart_item.product_variation.quantity:
            return JsonResponse({'message':"There is only " + str(cart_item.quantity) + " items in stock"}) 
        qty = cart_item.quantity + 1
        CartItem.objects.filter(id=cart_item.id).update(quantity=qty)
        cart_items = CartItem.objects.all().filter(user=request.user)
        updated_price = CartItem.objects.get(user=request.user, id=cart_item_id).sub_total()
        total_amount = 0
        for cart_item in cart_items:
            total_amount += cart_item.sub_total()
        return JsonResponse({'qty':qty, 'total_amount':total_amount,'updated_price':updated_price })
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        if cart_item.quantity + 1 > cart_item.product_variation.quantity:
            return JsonResponse({'message':"There is only " + str(cart_item.quantity) + " items in stock"})
        qty = cart_item.quantity + 1
        CartItem.objects.filter(id=cart_item_id).update(quantity=qty)
        cart_items = CartItem.objects.all().filter(cart=cart)
        updated_price = CartItem.objects.get(cart=cart, id=cart_item_id).sub_total()
        total_amount = 0
        for cart_item in cart_items:
            total_amount += cart_item.sub_total()
        return JsonResponse({'qty':qty, 'total_amount':total_amount,'updated_price':updated_price })



# Decrement cartitem quantity

def decrement_qty(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        qty = cart_item.quantity - 1
        CartItem.objects.filter(id=cart_item_id).update(quantity=qty)
        cart_items = CartItem.objects.all().filter(user=request.user)
        updated_price = CartItem.objects.get(user=request.user, id=cart_item_id).sub_total()
        total_amount = 0
        for cart_item in cart_items:
            total_amount += cart_item.sub_total()
        return JsonResponse({'qty':qty, 'total_amount':total_amount, 'updated_price':updated_price})
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
        qty = cart_item.quantity - 1
        CartItem.objects.filter(id=cart_item_id).update(quantity=qty)
        cart_items = CartItem.objects.all().filter(cart=cart)
        updated_price = CartItem.objects.get(cart=cart, id=cart_item_id).sub_total()
        total_amount = 0
        for cart_item in cart_items:
            total_amount += cart_item.sub_total()
        return JsonResponse({'qty':qty, 'total_amount':total_amount, 'updated_price':updated_price})
    

# Remove cartitem
def removeCartItem(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
    cart_item.delete()
    return JsonResponse({'message':'The item remove from cart'})



