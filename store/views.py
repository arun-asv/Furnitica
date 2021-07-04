from django.shortcuts import redirect, render
from .models import Category, Product
from .forms import CategoryForm, ProductForm
from django.http import HttpResponse, JsonResponse
from customer.models import Customer, Order
from django.contrib.auth.models import User, auth

# Create your views here.
def ad_login(request):
    return render(request, 'admin/login.html')

def ad_home (request):
    if request.method =='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password=password)
            if user.is_superuser:
                auth.login(request,user)
                return render (request, 'admin/index.html')
    elif request.user.is_authenticated:
        return render(request, 'admin/index.html')
    else:
        return redirect('ad_login')
    
def ad_user (request):
    if request.user.is_authenticated:
    
        customers = Customer.objects.all()

        return render(request, 'admin/user/usermanage.html', {'customers': customers})

def ad_product(request):
    if request.user.is_authenticated:
    
        products = Product.objects.all()

        return render(request, 'admin/product/productmanage.html', {'products': products})

def ad_category(request):
    if request.user.is_authenticated:
    
        categories = Category.objects.all()

        return render(request, 'admin/category/categorymanage.html', {'categories': categories})

def ad_order (request):
    if request.user.is_authenticated:
        orders = Order.objects.all()

        return render(request, 'admin/order/ordermanage.html', {'orders': orders})

def ad_offer(request):
    if request.user.is_authenticated:
        return render(request, 'admin/offer/offermanage.html')



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

def deletecategory(request, id):
    if request.user.is_authenticated:
        categories = Category.objects.get(pk=id)
    return render (request, 'admin/category/deletecategory.html', {'categories': categories})

def delete_cat(request, id):
    if request.user.is_authenticated:
        categories = Category.objects.filter(pk=id)
        categories.delete()
        return redirect ('categorymanage')

def nodelete_cat(request, id):
    if request.user.is_authenticated:
        categories = Category.objects.all()

        return render(request, 'admin/category/categorymanage.html', {'categories': categories})


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
def deleteproduct(request,id):
    if request.user.is_authenticated:
        product = Product.objects.filter(pk=id)
        product.delete()
        return render(request, 'admin/product/productmanage.html', {'product': product})
        
            

def block(request, id):
    if request.user.is_authenticated:
        user = Customer.objects.get(pk=id)
        user.is_active  = not (user.is_active)
        user.save()
        return redirect('usermanage')


def ad_search(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            searched = request.GET['searched']
            users = Customer.objects.filter(firstname__contains = searched)
            return render (request, 'admin/user/search.html', {'searched': searched, 'users': users})
        else:
            return redirect('ad_home')

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
        