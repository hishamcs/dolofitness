from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from product.models import Product,ProductVariation,Brand
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from orders.models import Order,OrderProduct
from .verify import send,check
from account.forms import RegistraionForm,AddressForm,UserProfileForm,UserForm
from account.models import Account,UserAddress,UserProfileImage,Wallet
from cart.models import Cart,CartItem
from cart.views import _cart_id
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
import random
import requests
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

# Create your views here.
def index(request):
    if request.user.is_superuser:
        pass
    if 'session' in request.session:
        return redirect('user_signup_otp')
    products = Product.objects.all().filter(is_available=True)
    pro_var = []
    for product in products:
        var = ProductVariation.objects.filter(product=product, is_active=True)
        for variation in var:
            pro_var.append(variation)

    product_variations = random.sample(pro_var, 8)
    brands = Brand.objects.all()
    context = {
        'product_variations':product_variations,
        'brands':brands,
    }
    return render(request, 'index.html',context)


def user_login(request):
    if request.user.is_superuser:
        return redirect('admin_home')
    if request.user.is_authenticated:
        return redirect('index')
    if 'session' in request.session:
        return redirect('user_signup_otp')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user is not None:
            if user.is_blocked:
                messages.warning(request,'You are Blocked by admin.please contact for further info')
                return redirect('user_login')
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items_guest = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for i in cart_items_guest:
                        product_variation.append(i.product_variation)
                    print('product variation : ', product_variation)
                    cart_items_user     = CartItem.objects.filter(user=user)
                    existing_var_list   = []
                    id = [] 
                    for i in cart_items_user:
                        existing_var_list.append(i.product_variation)
                        id.append(i.id)

                    for pr in product_variation:
                        if pr in existing_var_list:
                            cart_it = CartItem.objects.get(cart=cart,product_variation=pr)
                            index   = existing_var_list.index(pr)
                            item_id = id[index]
                            item    = CartItem.objects.get(id=item_id)
                            item.quantity += cart_it.quantity
                            item.user = user
                            item.save()
                            cart_it.delete()

                        else:
                            cart_item = CartItem.objects.get(cart=cart,product_variation=pr)
                            cart_item.user = user
                            cart_item.save()
            except:
                pass

            login(request,user)
            if request.user.is_superuser:
                return redirect('admin_home')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=')for x in query.split('&'))
                if 'next'in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
                return redirect('index')
        else:
            messages.error(request,'Invalid login credentials')
    return render(request,'login.html')


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    if 'session' in request.session:
        return redirect('user_signup_otp')
    if request.method == 'POST':
        form = RegistraionForm(request.POST)
        if form.is_valid():
            phone_number_with_country_code       = '+91'+form.cleaned_data['phone_number']
            request.session['phone_number'] = form.cleaned_data['phone_number']
            request.session['username']    = form.cleaned_data['username']
            request.session['email']       = form.cleaned_data['email']
            request.session['password']    = make_password(form.cleaned_data['password'])
            request.session['session']     = 'otp_verification'
            request.session.set_expiry(90)
            send(phone_number_with_country_code)
            messages.success(request,'An OTP is sent to the Phone Number')
            return redirect('user_signup_otp')
        else:
            messages.error(request,'Form is not valid, please fill the form correctly')
            form=RegistraionForm()
            return render(request,'signup.html',{'form':form})

    else:
        form=RegistraionForm()
    return render(request,'signup.html',{'form':form})


def user_signup_otp(request):
    if request.user.is_authenticated:
        return redirect('index')
    if 'session' in request.session:
        
        if request.method == 'POST':
            otp_code = request.POST['otp']
            print('otp : ',otp_code)
            print('phone : ',request.session['phone_number'])
            phone_number_with_country_code = '+91'+request.session['phone_number']
            if check(phone_number_with_country_code,otp_code):
                username = request.session['username']
                password = request.session['password']
                phone_number = request.session['phone_number']
                email = request.session['email']
                user = Account.objects.create_user(email=email,username=username,phone_number=phone_number)
                user.password=password
                user.save()
                print('user : ',user)
                userprofile = UserProfileImage.objects.create(user=user)
                userprofile.save()
                wallet = Wallet.objects.create(user=user)
                wallet.save()
                request.session.flush()
                messages.success(request,'Registraion is completed successfully...')
                return redirect('user_login')
            else:
                messages.error(request,'Invalid OTP')
                return redirect('user_signup_otp')
        return render(request,'signup_otp.html')

    return redirect('user_signup')


def user_logout(request):
    logout(request)
    return redirect('index')


def user_login_otp(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        # if not re.match(r'^[0-9]+$',phone_number):
        #     messages.error(request,'Phone number should contain only digits')
        # if len(phone_number)<10:
        #     messages.error(request,'Please provide a valid Phone number')
        if Account.objects.all().filter(phone_number=phone_number):
            phone_number_with_country_code='+91'+phone_number
            send(phone_number_with_country_code)
            return redirect(user_login_otp_verify,phone_number)
        else:
            messages.error(request,'Phone number is not registered with us')
    return render(request,'login_otp.html')


def user_login_otp_verify(request,phone_number):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        otp_code = request.POST['otp']
        phone_number_with_country_code = '+91'+phone_number
        if check(phone_number_with_country_code,otp_code):
            user = Account.objects.all().get(phone_number=phone_number)
            if user.is_blocked:
                messages.warning(request,'You are Blocked by admin.please contact for further info')
                return redirect('user_login_otp')
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'Incorrect OTP')

    return render(request,'login_otp_verify.html')


@login_required(login_url='user_login')
def dashboard(request):
    orders = Order.objects.order_by('-order_date').filter(user_id=request.user.id)
    wallet_amount = Wallet.objects.get(user_id = request.user.id).balance
    userprofile = UserProfileImage.objects.get(user=request.user)
    order_count = orders.count()
    context = {
        'wallet_amount':wallet_amount,
        'order_count':order_count,
        'user_profile':userprofile,
    }
    return render(request,'dashboard.html',context)

@login_required(login_url='user_login')
def edit_profile(request):
    if request.method == 'POST':
        userprofileimage = UserProfileImage.objects.get(user=request.user)
        form = UserProfileForm(request.POST,request.FILES,instance=userprofileimage)
        userform = UserForm(request.POST, instance=request.user)
        
        if form.is_valid() and userform.is_valid():
            form.save()
            userform.save()
            # userprofileimage = UserProfileImage()
            #---------------------------------------
            # userprofileimage.user = request.user
            # userprofileimage.first_name = form.cleaned_data['first_name']
            # userprofileimage.last_name = form.cleaned_data['last_name']
            # userprofileimage.profile_pic = form.cleaned_data['profile_pic']
            # userprofileimage.save()
            #--------------------------------------
            # serialized_data = serializers.serialize('json', [userprofileimage])
            # return JsonResponse(serialized_data, safe=False)
            
            response_data = {
                'first_name':userprofileimage.first_name,
                'last_name':userprofileimage.last_name,
                # 'profile_pic':userprofileimage.profile_pic.url,
            }
            return JsonResponse(response_data)
        else:
            print('form is not valid')
            print(form.errors)
            print(userform.errors)
    userform = UserForm(instance=request.user)
    user_profile = UserProfileImage.objects.get(user=request.user)   
    userprofileform = UserProfileForm(instance=user_profile)
    
    context = {
        'userprofileform':userprofileform,
        'user_profile':user_profile,
        'userform':userform,
    }
    return render(request,'editprofile.html',context)


@login_required(login_url='user_login')
def get_address(request,address_id):
    try:
        address = UserAddress.objects.get(id=address_id)
        address_data = {
            'first_name':address.first_name,
            'last_name':address.last_name,
            'email':address.email,
            'address_line1':address.address_line1,
            'address_line2':address.address_line2,
            'phone':address.phone,
            'city':address.city,
            'state':address.state,
            'country':address.country,
            'postcode':address.postcode,
        }
        return JsonResponse(address_data)
    except UserAddress.DoesNotExist:
        return JsonResponse({'error':'Address not found'}, status=404)
    



@login_required(login_url='user_login')
def del_addr(request,address_id):
    
    try:
        address = UserAddress.objects.get(id=address_id)
        address.delete()
        return JsonResponse({'msg':'Deleted successfully'})
    except UserAddress.DoesNotExist:
        pass


# Default address
@login_required(login_url='user_login')
def set_default_addr(request,address_id):
    print('request.GET : ',request.GET)
    print('address id : ',address_id)
    UserAddress.objects.filter(user=request.user,default_addr=True).update(default_addr=False)
    UserAddress.objects.filter(pk=address_id,user=request.user).update(default_addr=True)
    return JsonResponse({'msg':'success'})



@login_required(login_url='user_login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {
        'orders':orders,
    }
    return render(request,'my-orders.html',context)

@login_required(login_url='user_login')
def user_order_details(request,order_id):
    print('order id : ', order_id)
    order = Order.objects.get(id=order_id,user=request.user)
    orderproducts = OrderProduct.objects.filter(order=order)
    context = {
        'order':order,
        'orderproducts':orderproducts,
    }
    return render(request, 'order_detail.html', context)







# change password
@login_required(login_url='user_login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']

        user = Account.objects.get(username__exact=request.user.username)
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully')
            return redirect('change_password')
        else:
            messages.error(request, 'Please enter valid current Password')
            return redirect('change_password')
    return render(request, 'change_password.html')


# invoice generation

def invoice(request, order_item_id):
    print('orderitem id : ', order_item_id)
    ordered_product = OrderProduct.objects.get(id=order_item_id, order__user=request.user)
    context = {
        'item':ordered_product,
        'discount':0,
    }
    return render(request,'invoice.html',context)


#download invoice

from io import BytesIO
from xhtml2pdf import pisa
from django.views.generic import View
from django.template.loader import get_template



class generateInvoice(View):

    def get(self, request, orderitem_id, *args, **kwargs):
        try:
            orderproduct = OrderProduct.objects.get(id=orderitem_id)
        except:
            return HttpResponse('505 not found')
        context = {
            'item':orderproduct,
            'discount':0,
        }
        
        pdf = render_to_pdf('printinvoice.html',context)
        return HttpResponse(pdf, content_type='application/pdf')
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# test 
@login_required(login_url='user_login')
def my_address(request):
    
    
    if request.method == "POST":

        address_id = request.POST['addr_id']
        if address_id == '':
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()
                return JsonResponse({'title':'Success', 'text':'Address Updated','icon':'success'})
            else:
                return JsonResponse({'title':'Error', 'text':'Please fill the enter valid address','icon':'warning'})

        else:
            
            address = UserAddress.objects.get(id=address_id)
            
            form = AddressForm(request.POST,instance=address)
            if form.is_valid():
                form.save()
                return JsonResponse({'title':'Success', 'text':'Address Updated','icon':'success'})
            else:
                return JsonResponse({'title':'Error', 'text':'Please fill the enter valid address','icon':'warning'})

        #form = AddressForm(request.POST)
        # if form.is_valid():
        #     address = form.save(commit=False)
        #     address.user = request.user
        #     address.save()
        #     return JsonResponse({'msg':'success'})
    addresses = UserAddress.objects.all().filter(user=request.user)
    form = AddressForm()
    context = {
        'form':form,
        'addresses':addresses,
    }
    return render(request,'my_address.html',context)

@never_cache
def forgotpassword(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        try:
            user = Account.objects.get(phone_number=phone_number)
            phnum_with_cntry_code = '+91' + phone_number
            send(phnum_with_cntry_code)
            return JsonResponse({'status':'success', 'message':'OTP send successfully'})
        except Account.DoesNotExist:
            return JsonResponse({'status':'error', 'message':'user is not found...'})
    
    return render(request, 'forgotpassword.html')

@never_cache
def verify_otp_password(request):
    otp = request.POST.get('otp')
    phone = request.POST.get('phone_number')
    if phone is None:
        return redirect('forgotpassword')
    phnum_with_cntry_code = '+91' + phone
    print('phone : ', phone)
    print('otp : ', otp)
    if check(phnum_with_cntry_code, otp):
        return render(request,'forgotpass-reset.html',{'phone':phone})
    elif otp is None:
        return redirect('forgotpassword')
    else:
        messages.error(request, 'The entered OTP is invalid')
        return redirect('forgotpassword')

@never_cache
def reset_passw_forget(request):
    if request.method == 'POST':
        passw = request.POST.get('new_password')
        phone_num = request.POST.get('phone_num')
        user = Account.objects.get(phone_number=phone_num)
        user.set_password(passw)
        user.save()
        messages.success(request, 'Password Reseted Successfully...')
        return redirect('user_login')
    else:
        return redirect('forgotpassword')
    


def error_404(request, exception):
    if request.path.startswith('/adminn/'):
        return render(request, 'admn/ad_error_404.html')
    return render(request, 'user_404.html')



