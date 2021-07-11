from django.shortcuts import redirect, render
from .models import Category, Product
from customer.models import Coupon
from customer.forms import CouponForm
from .forms import CategoryForm, ProductForm
from django.http import HttpResponse, JsonResponse
from customer.models import Customer, Order
from django.contrib.auth.models import User, auth

# Create your views here.
def ad_login(request):
    return render(request, 'admin/login.html')

def ad_home (request):
    users= Customer.objects.all().count()
    orders = Order.objects.all().count()
    products = Product.objects.all().count()
    order_placed = Order.objects.filter(status='Placed').count()
    order_shipped = Order.objects.filter(status='Shipped').count()
    order_delivered = Order.objects.filter(status='Delivered').count()
    total_price = Order.objects.all()
    total = 0
    for o in total_price:
        total += o.price
    if request.method =='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password=password)
            if user:
                auth.login(request,user)
                return render (request, 'admin/index.html', {'users': users, 'orders': orders, 'order_placed': order_placed, 'order_shipped': order_shipped, 'order_delivered': order_delivered, 'total': total})
                

                
                
            else:
                return redirect('ad_login')
    elif request.user.is_authenticated:
        return render (request, 'admin/index.html', {'users': users, 'orders': orders, 'order_placed': order_placed, 'order_shipped': order_shipped, 'order_delivered': order_delivered, 'total': total})
    else:
        return redirect('ad_login')
    
def ad_user (request):
    if request.user.is_authenticated:
    
        customers = Customer.objects.all()

        return render(request, 'admin/user/usermanage.html', {'customers': customers})
    else:
        return redirect ('ad_login')

def ad_product(request):
    if request.user.is_authenticated:
    
        products = Product.objects.all()

        return render(request, 'admin/product/productmanage.html', {'products': products})
    else:
        return redirect ('ad_login')

def ad_category(request):
    if request.user.is_authenticated:
    
        categories = Category.objects.all()

        return render(request, 'admin/category/categorymanage.html', {'categories': categories})
    else:
        return redirect ('ad_login')

def ad_order (request):
    if request.user.is_authenticated:
        orders = Order.objects.all()

        return render(request, 'admin/order/ordermanage.html', {'orders': orders})
    else:
        return redirect ('ad_login')

def ad_offer(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        product = Product.objects.all()
        coupon = Coupon.objects.all()
        return render(request, 'admin/offer/offermanage.html', {'categories': category, 'products': product, 'coupons': coupon})
    else:
        return redirect ('ad_login')



def newcategory(request):
    if request.user.is_authenticated:
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('categorymanage')
        else:
            form = CategoryForm
            context = {'form': form}
            return render(request, 'admin/category/addcategory.html', context)
    else:
        return redirect ('ad_login')

def editcategory(request, id):
    if request.user.is_authenticated:
        categories = Category.objects.get(pk=id)
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES, instance = categories)

            if form.is_valid():
                form.save()
                return redirect('categorymanage')
        
        else:
            form = CategoryForm(instance = categories)
            return render(request, 'admin/category/editcategory.html', {'form': form, 'categories': categories})

def deletecategory(request,id):
    if request.user.is_authenticated:
        category = Category.objects.filter(pk=id)
        category.delete()
        return redirect('categorymanage')


def newproduct(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                print('working')
                return redirect ('productmanage')
        
    
        
            else:
                form = ProductForm()
                posts = Product.objects.all()
                return render(request, 'admin/product/addproduct.html', {'form': form, 'posts': posts})
        else:
            form = ProductForm()
            posts = Product.objects.all()
            return render(request, 'admin/product/addproduct.html', {'form': form, 'posts': posts})
        
    
def editproduct(request, id):
    if request.user.is_authenticated:
        products = Product.objects.get(pk=id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance = products)

            if form.is_valid():
                form.save()
                return redirect('productmanage')
        
        else:
            form = ProductForm(instance = products)
            return render(request, 'admin/product/editproduct.html', {'form': form, 'products': products})
    else:
        return render('ad_login')
def deleteproduct(request,id):
    if request.user.is_authenticated:
        product = Product.objects.filter(pk=id)
        product.delete()
        return redirect('productmanage')
    else:
        return render('ad_login')
        
            

def block(request, id):
    if request.user.is_authenticated:
        user = Customer.objects.get(pk=id)
        user.is_active  = not (user.is_active)
        user.save()
        return redirect('usermanage')
    else:
        return render('ad_login')



def admin_order_status(request):
    if request.user.is_authenticated:
        order_id = request.POST['order_id']
        value = request.POST['clicked']
        this_order = Order.objects.get(pk=order_id)
        if request.POST['clicked'] == 'Shipped':
            this_order.status = 'Shipped'
            this_order.save()
        elif request.POST['clicked'] == 'Delivered':
            this_order.status = 'Delivered'
            this_order.save()
        return JsonResponse('true', safe=False)
    else:
        return render('ad_login')

def cancel_order(request, id):
    order = Order.objects.get(id=id)
    order.status = 'Canceled'
    print('cancel')
    order.save()
    return redirect('ordermanage')

def addcoupon(request):
     if request.user.is_authenticated:
        form = CouponForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('ad_offer')
        else:
            form = CouponForm()
            context = {'form': form}
            return render(request, 'admin/offer/addcoupon.html', context)
     else:
        return render('ad_login')

def deletecoupon(request, id):
    if request.user.is_authenticated:
        coupon = Coupon.objects.filter(id=id)
        coupon.delete()
        return redirect('ad_offer')
    else:
        return render('ad_login')

def cat_offer(request, id):
    if request.user.is_authenticated:
        category = Category.objects.get(id=id)
        return render(request, 'admin/offer/cat_offer.html', {'category': category})
    else:
        return render('ad_login')



def pro_offer(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        return render(request, 'admin/offer/pro_offer.html', {'product': product})
    else:
        return render('ad_login')

def offer_cat(request, id):
    if request.user.is_authenticated:
        if request.method=='POST':
            offer = request.POST['offer']
            cat = Category.objects.get(id=id)
            cat.offer = int(offer)
            cat.save()
            print('working')
            return redirect('ad_offer')
    else:
        return redirect('ad_login')

def offer_pro(request, id):
    if request.user.is_authenticated:
        if request.method=='POST':
            offer = request.POST['offer']
            pro = Product.objects.get(id=id)
            pro.offer = int(offer)  
            pro.save()
            return redirect('ad_offer')
    else:
        return redirect('ad_login')

def report(request,total=0, quantity=0, cart_items=None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            date_from=request.POST['datefrom']
            date_to=request.POST['dateto']
            order_search=Order.objects.filter(start_date__range=[date_from,date_to])
            return render(request,'admin/order/report.html',{'orders':order_search})
        else:
            orders = Order.objects.all()
            return render(request,'admin/order/report.html',{"orders":orders})
    else:
        return redirect('ad_login')


