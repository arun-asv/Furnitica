from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, Category
from . models import Customer, Otp, CartItem, Order
from django.contrib import messages
from .forms import AddressForm
from .models import Address
import razorpay
from twilio.rest import Client

# Create your views here.

def register (request):
    return render (request, 'user/user-register.html')

def login (request):
    return render (request, 'user/user-login.html')


def home (request):
    if request.session.has_key('username'):
        queryset = Product.objects.all()
        querycat = Category.objects.all()
        uname = request.session['username']
        user =  Customer.objects.get(username = uname)
        context = {'products': queryset, 'categories': querycat, 'user': user}
        return render(request, 'user/home.html', context)
    else:
        return redirect('landing')
    
    
def productdetail(request, id):
    if request.session.has_key('username'):
        uname = request.session['username']
        user =  Customer.objects.get(username = uname)
        product = Product.objects.get(pk = id)
        return render(request, 'user/product-detail.html', {'product': product, 'user': user})
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
        user = Customer.objects.get(number = num)
        if user.is_active:
            request.session['username'] = user.username
            request.session['otp'] = num
            print('working')
            account_sid = 'AC10e0c475ec2f539d15cbcc1abc7bac02'
            auth_token = '35f542262d0a52c99ecacb466c62f2e5'
            client = Client(account_sid, auth_token)

            verification = client.verify \
                .services('VA5b2cb2faa881dc4a1e101b8954ed9add') \
                    .verifications \
                        .create(to='+91'+num, channel='sms')

        print(verification.status)
        return render (request, 'user/otp.html', {'num' : num})
        
def verify (request, num):
    if request.method =='POST':
        otp = request.POST['otp']
        num = request.session['otp']
        uname = request.session['username']
        user = Customer.objects.get(username=uname)
        account_sid = 'AC10e0c475ec2f539d15cbcc1abc7bac02'
        auth_token = '35f542262d0a52c99ecacb466c62f2e5'
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                           .services('VA5b2cb2faa881dc4a1e101b8954ed9add') \
                           .verification_checks \
                           .create(to='+91'+num, code=otp)

        print(verification_check.status)
        if verification_check.status =='approved':
            return redirect('home')

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        


        user = Customer.objects.get(username = username, password = password)
        if user.is_active:
                request.session['username']= user.username
                return redirect ('home')
        
        else: 
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
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            user=user
        )
        cart_item.save()
    return JsonResponse({})

        

def cart(request, total = 0, quantity =0, cart_item = None):

        if request.session.has_key('username'):
            uname = request.session['username']
            user = Customer.objects.get(username=uname)
            cart_items = CartItem.objects.filter(user=user)
        
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
                print(cart_item.id)

        context = {
            'total' : total,
            'quantity': quantity,
            'cart_items': cart_items,
            'user' : user,
            }
        return render (request, 'user/product-cart.html', context)



def remove_cart (request):
    if request.method == 'GET':
        id = int(request.GET['cid'])
    
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_item = CartItem.objects.get(id=id, user=user)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    
    total=0
    mcart = CartItem.objects.filter(user=user)
    for i in mcart:
        total += (i.product.price * i.quantity)
    cart_item.sub_total = cart_item.product.price * cart_item.quantity
    data={
        'qty':cart_item.quantity,
        'sub':cart_item.sub_total,
        'total':total
    }
    
    return JsonResponse(data)

def incre_cart(request):
    if request.method == 'GET':
        id = int(request.GET['cid'])
    
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_item = CartItem.objects.get(id=id, user=user)
    cart_item.quantity += 1
    cart_item.save()
    total=0
    mcart = CartItem.objects.filter(user=user)
    for i in mcart:
        total += (i.product.price * i.quantity)
    cart_item.sub_total = cart_item.product.price * cart_item.quantity
    data={
        'qty':cart_item.quantity,
        'sub':cart_item.sub_total,
        'total':total
    }


    return JsonResponse(data)


def remove_cart_item(request, id):
    
    uname = request.session['username']
    print(uname)

    user = Customer.objects.get(username=uname)
    cart_item = CartItem.objects.get(id=id, user=user)
    cart_item.delete()
    return redirect ('cart')

def my_account(request):
    if request.session.has_key('username'):
        uname = request.session['username']
        user = Customer.objects.get(username = uname)
        return render(request, 'user/user-account.html', {'user': user})
    else:
        return redirect('landing')



def checkout(request, total=0, quantity = 0, cart_items=None):
    if request.session.has_key('username'):
        uname = request.session['username']
        user = Customer.objects.get(username=uname)
        cart_items = CartItem.objects.filter(user=user)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity        


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
            'user' : user


        }

    
        return render(request, 'user/product-checkout.html', context)
    else:
        return redirect('landing')


def address(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            form = AddressForm(request.POST)

            if form.is_valid():
                if request.POST.get('check'):
                    newaddress = form.save(commit=False)
                    uname = request.session['username']
                    user = Customer.objects.get(username = uname)

                    newaddress.user = user
                    newaddress.save()
                    return redirect('checkout')
                else:
                    request.session['fullname'] = request.POST['fullname']
                    request.session['pincode'] = request.POST['pincode']
                    request.session['email'] = request.POST['email']
                    request.session['address1'] = request.POST['address1']
                    request.session['address2'] = request.POST['address2']
                    request.session['landmark'] = request.POST['landmark']
                    request.session['country'] = request.POST['country']
                    return redirect ('checkout')

               

        else:
            form = AddressForm
            context = {'form': form}
            return render(request, 'user/product-checkout.html', context)
    else:
        return redirect('landing')

    return redirect('checkout')

def place_order(request, total =0, quantity = 0):
    if request.session.has_key('username'):
       
            if request.POST.get('address'):
        
                delivery_address = Address.objects.get(id=request.POST.get('address'))
                uname = request.session['username']
                user = Customer.objects.get(username=uname)
                cart_items = CartItem.objects.filter(user=user)
        
                for cart_item in cart_items:
                    total += (cart_item.product.price * cart_item.quantity)
                    quantity += cart_item.quantity     
                
                request.session['total'] = total
            else:
                fullname = request.session['fullname']
                pincode = request.session['pincode']
                email = request.session['email']
                address1 = request.session['address1']
                address2 = request.session['address2']
                landmark = request.session['landmark'] 
                country = request.session['country']
                uname = request.session['username']
                user = Customer.objects.get(username = uname)
                delivery_address = Address.objects.create(user=user, fullname=fullname, pincode=pincode, email=email, address1=address1, address2=address2, landmark=landmark, country=country)
                
                cart_items = CartItem.objects.filter(user=user)
                for cart_item in cart_items:
                    total += (cart_item.product.price * cart_item.quantity)
                    quantity += cart_item.quantity
                request.session['total'] = total
    
    amount = request.session['total']
    rupee = float(amount)*100
    request.session['payment_method'] = 'RazorPay'
    request.session['pay_method'] ='PayPal'
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_TIe1prjDi1KTsV", "E2hwXHOnGfOot7uO5AokFNeB"))
    payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})  
            
    context = {
    'delivery_address': delivery_address,
    'cart_items': cart_items,
    'total': total,
    'rupee': rupee,
    'user' : user

    }
    return render (request, 'user/payment.html', context)

def success(request, total=0, quantity=0):
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_items = CartItem.objects.filter(user=user)
        
    for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        
    order = Order.objects.create(user=user, item=cart_item, price=total, status= 'Placed')
    order.save()
        
    return render(request, 'user/success.html')

def successrazorpay(request, total=0, quantity=0):
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_items = CartItem.objects.filter(user=user)
        
    for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    pay_method = request.session['payment_method']
    
        
    order = Order.objects.create(user=user, item=cart_item, price=total, status= 'Placed', pay_method = pay_method)
        
    order.save()
        
    return render(request, 'user/success.html')

def successpaypal(request, total=0, quantity=0):
    uname = request.session['username']
    user = Customer.objects.get(username=uname)
    cart_items = CartItem.objects.filter(user=user)
        
    for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    pay_method = request.session['pay_method']
    uname = request.session['username']
    user = Customer.objects.get(username = uname)
        
    order = Order.objects.create(user=user, item=cart_item, price=total, status= 'Placed', pay_method = pay_method)
    order.save()
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