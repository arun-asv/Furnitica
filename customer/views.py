from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, Category
from . models import Cart_count, Customer, Otp, CartItem, Order
from django.contrib import messages
from .forms import AddressForm
from .models import Address, Coupon
import razorpay
from twilio.rest import Client
from decouple import config

# Create your views here.

def register (request):
    return render (request, 'user/user-register.html')

def login (request):
    return render (request, 'user/user-login.html')


def home (request):
    if request.session.has_key('username'):
        uname = request.session['username']
        user =  Customer.objects.get(username = uname)
        queryset = Product.objects.all()
        querycat = Category.objects.all()
        for p in queryset:
            if p.offer > p.category.offer:
                p.finalprice = p.price-(p.offer*p.price/100)
            elif p.offer <= p.category.offer:
                p.finalprice = p.price-(p.category.offer*p.price/100)
            p.save()
        try:
            count = Cart_count.objects.get(user=user)
            cartcount = count.count
        except:
            cartcount = 0
        prolist=Product.objects.all().order_by('date_posted')
        
        context = {'products': prolist, 'categories': querycat, 'user': user, 'c': cartcount}
        return render(request, 'user/home.html', context)
    else:
        return redirect('landing')

def categories(request,id):
    if request.session.has_key('username'):
        uname = request.session['username']
        user =  Customer.objects.get(username = uname)
        category = Category.objects.get(id=id)
        product = Product.objects.filter(category=category)
        return render(request, 'user/categories.html', {'user': user, 'products': product})
    else:
        return redirect('landing')

    
    
def productdetail(request, id):
    if request.session.has_key('username'):
        uname = request.session['username']
        user =  Customer.objects.get(username = uname)
        product = Product.objects.get(pk = id)
        try:
            count = Cart_count.objects.get(user=user)
            cartcount = count.count
        except:
            cartcount = 0
        
        return render(request, 'user/product-detail.html', {'product': product, 'user': user, 'c': cartcount})
    else:
        return redirect('landing')



def landing (request):
    queryset = Product.objects.all()
    querycat = Category.objects.all()
    context = {'products': queryset, 'categories': querycat}
    return render(request, 'user/index.html', context)

def sendotp(request):
    if request.method =='POST':
        num = request.POST['number']
        if Customer.objects.filter(number=num):
            user = Customer.objects.get(number = num)
            if user.is_active:
                request.session['username'] = user.username
                request.session['otp'] = num
                print('working')
                account_sid = config ('account_sid')
                auth_token = config ('auth_token')
                client = Client(account_sid, auth_token)

                verification = client.verify \
                .services('VA34e1e5f805fb28eb6f0931e387ea10cb') \
                    .verifications \
                        .create(to='+91'+num, channel='sms')
        

            print(verification.status)
            return render (request, 'user/otp.html', {'num' : num})
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect ('login')

        
def verify (request, num):
    if request.method =='POST':
        otp = request.POST['otp']
        num = request.session['otp']
        uname = request.session['username']
        user = Customer.objects.get(username=uname)
        account_sid = 'AC6d38580f9777da660b0aa694585250ff'
        auth_token = '9970f085b20acf924e7ef584ac471b42'
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                           .services('VA34e1e5f805fb28eb6f0931e387ea10cb') \
                           .verification_checks \
                           .create(to='+91'+num, code=otp)

        print(verification_check.status)
        if verification_check.status =='approved':
            return redirect('home')

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if Customer.objects.filter(username = username, password = password).exists():
            user = Customer.objects.get(username = username, password = password)
            
            
            if user.is_active:
                request.session['username']= user.username
                return redirect ('home')
        
            
        
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect ('login')
    
    else:
        return redirect('login')


def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        username = request.POST['username']
        number = request.POST['number']

        if password1 == password2:
            if Customer.objects.filter(email=email).exists():
                messages.error(request, 'email already exists', extra_tags ='signup')
                return redirect('register')
            elif Customer.objects.filter(username = username).exists():
                 messages.error(request, 'username already exists', extra_tags ='signup')
            
            elif Customer.objects.filter(number=number).exists():
                messages.error(request, 'mobile number already exists', extra_tags='signup')
                return redirect ('register')
            

            else:
                user = Customer.objects.create(password=password1, email=email, firstname=firstname, lastname=lastname, number=number, username = username)
                print ('saved')
                user.save()
                request.session['username'] = user.username
                return redirect ('home')
        else:
            messages.error(request, 'password does not match', extra_tags ='signup')
            return redirect('register')

def offerstore(request):
    if request.session.has_key('username'):
        products = Product.objects.filter(offer__range=[1, 95])
        return render(request, 'user/offerstore.html', {'products': products})

def logout(request):
    if request.session.has_key('username'):
        request.session.flush()
        return redirect('landing')
    else:
        return redirect ('home')



def add_cart(request):
    id = int(request.GET['product_id'])
    product = Product.objects.get(id = id)
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    
   
    if CartItem.objects.filter(product=product, user=user).exists():
        cart_item = CartItem.objects.get(product=product, user=user)  
        cart_item.quantity +=1
        cart_item.save()
    
    else:
        cart_item = CartItem.objects.create(user=user, product=product, quantity=1)
        cart_item.save()

    if Cart_count.objects.filter(user=user).exists():
        count = Cart_count.objects.get(user=user)
        cc = int(count.count)
        cc +=1
        count.count = str(cc)
        count.save()
        
    else:
        
        count = Cart_count.objects.create(user=user, count=1)
        count.save()
        count.count = 1
    return JsonResponse({'c': count.count })

        

def cart(request, total = 0, quantity =0, cart_item = None):

        if request.session.has_key('username'):
            uname = request.session['username']
            user = Customer.objects.get(username=uname)
            cart_items = CartItem.objects.filter(user=user)
        
            for cart_item in cart_items:
                total += (cart_item.product.finalprice * cart_item.quantity)
                quantity += cart_item.quantity
                print(cart_item.id)
            try:
                count = Cart_count.objects.get(user=user)
                cartcount = count.count
            except:
                
                cartcount = 0
            

        context = {
            'total' : total,
            'quantity': quantity,
            'cart_items': cart_items,
            'user' : user,
            'c': cartcount
            }
        return render (request, 'user/product-cart.html', context)



def remove_cart (request):
    if request.method == 'GET':
        id = int(request.GET['cid'])
    
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_item = CartItem.objects.get(id=id, user=user)
    count = Cart_count.objects.get(user=user)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cc = int(count.count)
        cc -= 1
        count.count = str(cc)
        count.save()
        cart_item.save()
    
    total=0
    mcart = CartItem.objects.filter(user=user)
    for i in mcart:
        total += (i.product.finalprice * i.quantity)
    cart_item.sub_total = cart_item.product.finalprice * cart_item.quantity
    data={
        'qty':cart_item.quantity,
        'sub':cart_item.sub_total,
        'total':total,
        'c': count.count,

    }
    
    return JsonResponse(data)

def incre_cart(request):
    if request.method == 'GET':
        id = int(request.GET['cid'])
    
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_item = CartItem.objects.get(id=id, user=user)
    count = Cart_count.objects.get(user=user)
    cart_item.quantity += 1
    cc = int(count.count)
    cc += 1
    count.count = str(cc)
    count.save()
    cart_item.save()
    total=0
    mcart = CartItem.objects.filter(user=user)
    for i in mcart:
        total += (i.product.finalprice * i.quantity)
    cart_item.sub_total = cart_item.product.finalprice * cart_item.quantity
    data={
        'qty':cart_item.quantity,
        'sub':cart_item.sub_total,
        'total':total,
        'c': count.count
    }


    return JsonResponse(data)


def remove_cart_item(request, id):
    
    uname = request.session['username']
    print(uname)

    user = Customer.objects.get(username=uname)
    cart_item = CartItem.objects.get(id=id, user=user)
    count = Cart_count.objects.get(user=user)
    cc = int(count.count)
    cc -= cart_item.quantity
    count.count = str(cc)
    count.save()
    cart_item.delete()
    return redirect ('cart')
    
def my_account(request):
    
    if request.session.has_key('username'):
        uname = request.session['username']
        user = Customer.objects.get(username = uname)
        ord = Order.objects.filter(user=user)
        context = { 'user' : user, 'ord': ord}
        return render(request, 'user/user-account.html', context)
    else:
        return redirect('landing')

def editprofile(request, id):
    if request.session.has_key('username'):
        user = Customer.objects.get(id=id)
        return render(request, 'user/editprofile.html', {'user': user})

def saveprofile(request):
    if request.method=='POST':
        id = request.POST['hidden']
        firstname = request.POST['firstname']
        email = request.POST['email']
        image = request.FILES.get('image')
        print(image)
        Customer.objects.filter(id=id).update(firstname=firstname, email=email)
        if image is not None:
            user = Customer.objects.get(id=id)
            user.image = image
            user.save()
        return redirect('my_account')
        
        
    

def checkout(request, total=0, quantity = 0, cart_items=None):
    if request.session.has_key('username'):
        uname = request.session['username']
        user = Customer.objects.get(username=uname)
        cart_items = CartItem.objects.filter(user=user)
        try:
            count = Cart_count.objects.get(user=user)
            cartcount = count.count
        except:
                
                cartcount = 0
        
        for cart_item in cart_items:
            total += (cart_item.product.finalprice * cart_item.quantity)
            quantity += cart_item.quantity
        request.session['gtotal']=total     


        form = AddressForm()
       
        
    
        uname = request.session['username']
        user = Customer.objects.get(username = uname)
        queryset = Address.objects.all().filter(user = user)

        context = {
            'total' : total,
            'form' : form,
            'quantity': quantity,
            'cart_items': cart_items,
            'addresses' : queryset,
            'user' : user,
            'c': cartcount


        }

    
        return render(request, 'user/product-checkout.html', context)

def address(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            form = AddressForm(request.POST)

            if form.is_valid():
                
                    newaddress = form.save(commit=False)
                    uname = request.session['username']
                    user = Customer.objects.get(username = uname)
                    print('hi')
                    newaddress.user = user
                    newaddress.save()
                    return redirect('checkout')
               

               

        else:
            form = AddressForm
            context = {'form': form}
            return render(request, 'user/product-checkout.html', context)
    else:
        return redirect('landing')

    return redirect('checkout')

def apply_coupon(request):
    if request.method =='GET':
        code = request.GET['ccode']
        print(code)
        gtotal = int(request.GET['gtotal'])
        uname = request.session['username']
        user = Customer.objects.get(username=uname)

        if Coupon.objects.filter(code=code).exists():
            coupon = Coupon.objects.get(code=code)
            if Order.objects.filter(coupon=coupon, user=user).exists():
                messages.info(request, 'Coupon already taken')
                return redirect('checkout')
            else:
                gtotal = gtotal-(gtotal*coupon.dis/100)
                request.session['coup_id'] = coupon.id
        request.session['gtotal']=int(gtotal)
        data = {'gtotal': gtotal}
        return JsonResponse(data)





def place_order(request, total =0, quantity = 0):

    if request.session.has_key('username'):

            if request.POST.get('address'):
                try:
                    delivery_address = Address.objects.get(id=request.POST.get('address'))
                except:
                    return redirect('checkout')
                uname = request.session['username']
                user = Customer.objects.get(username=uname)
                cart_items = CartItem.objects.filter(user=user)
                try:
                    count = Cart_count.objects.get(user=user)
                    cartcount = count.count
                except:
                
                    cartcount = 0
                
        
                
    amount = request.session['gtotal']
    rupee = float(amount)*100
    request.session['payment_method'] = 'RazorPay'
    request.session['pay_method'] ='PayPal'
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_YlEKO49r8wFNDh", "2Lhy5RpKcilXX7UceBvSkPUE"))
    payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})  
            
    context = {
    'delivery_address': delivery_address,
    'cart_items': cart_items,
    'total': amount,
    'rupee': rupee,
    'user' : user,
    'c' : count,

    }
    return render (request, 'user/payment.html', context)

def success(request, total=0, quantity=0):

    uname = request.session['username']
    print(uname)
    user = Customer.objects.get(username=uname)
    cart_items = CartItem.objects.filter(user=user)
    cartcount = Cart_count.objects.filter(user=user)
    print('work')
        
    for cart_item in cart_items:
            total = (cart_item.product.finalprice * cart_item.quantity)
            quantity = cart_item.quantity
            if request.session. has_key('coup_id'):
                cid = request.session['coup_id']
                coup = Coupon.objects.get(id=cid)
                pri = int(cart_item.sub_total())-(int(cart_item.sub_total())*coup.dis/100)
            
                order = Order.objects.create(user=user, item=cart_item.product, price=pri, status= 'Placed')
            else:
                order = Order.objects.create(user=user, item=cart_item.product, price=total, status='Placed')
            order.save()
            cart_item.delete()
            cartcount.delete()
        
    return render(request, 'user/success.html')

def successrazorpay(request, total=0, quantity=0):
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_items = CartItem.objects.filter(user=user)
    cartcount = Cart_count.objects.filter(user=user)
        
    for cart_item in cart_items:
            total += (cart_item.product.finalprice * cart_item.quantity)
            quantity += cart_item.quantity
            pay_method = request.session['payment_method']
            if request.session. has_key('coup_id'):
                cid = request.session['coup_id']
                coup = Coupon.objects.get(id=cid)
                pri = int(cart_item.sub_total())-(int(cart_item.sub_total())*coup.dis/100)
                order = Order.objects.create(user=user, item=cart_item.product, price=pri, status= 'Placed', pay_method = pay_method)
            else:
                order = Order.objects.create(user=user, item=cart_item.product, price=total, status = 'Placed', pay_method= pay_method)
        
            order.save()
            cart_item.delete()
            cartcount.delete()

        
    return render(request, 'user/success.html')

def successpaypal(request, total=0, quantity=0):
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_items = CartItem.objects.filter(user=user)
    cartcount = Cart_count.objects.filter(user=user)
        
    for cart_item in cart_items:
            total += (cart_item.product.finalprice * cart_item.quantity)
            quantity += cart_item.quantity
            pay_method = request.session['pay_method']
            if request.session. has_key('coup_id'):
                cid = request.session['coup_id']
                coup = Coupon.objects.get(id=cid)
                pri = int(cart_item.sub_total())-(int(cart_item.sub_total())*coup.dis/100)
                order = Order.objects.create(user=user, item=cart_item.product, price=pri, status= 'Placed', pay_method = pay_method)
            else:
                order = Order.objects.create(user=user, item=cart_item.product, price=total, status='Placed', pay_method=pay_method)
            order.save()
            cart_item.delete()
            cartcount.delete()
    return render(request, 'user/success.html')

def order_status(request):
    order_id = request.POST['order_id']
    value = request.POST['clicked']
    this_order = Order.objects.get(pk=order_id)
    if value == 'Cancel':
        this_order.status = 'Canceled'
        this_order.save()
    elif value == 'Return':
        this_order.status = 'Returned'
        this_order.save()
    return JsonResponse('true', safe=False)