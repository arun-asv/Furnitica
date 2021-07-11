from django.db import models
from django.db.models.deletion import CASCADE
from twilio.rest import Client
import random
from store.models import Product
import uuid
from django.utils import timezone



# Create your models here.

class Customer(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200) 
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=50)
    number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'pics/pro', null=True)
    
    
    

    def __str__(self):
        return self.firstname


class Otp(models.Model):
    num = models.IntegerField()
    validnum = random.randint(1000, 9999)
    vnum = validnum

    def __str__(self):
        return self.num



class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    
    
    def sub_total(self):
        return self.product.finalprice * self.quantity

    def __str__(self):
        return self.product.product_name


class Address(models.Model):
    user = models.ForeignKey(Customer, on_delete=CASCADE)
    fullname = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    mobile = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    landmark = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    check = models.BooleanField(default = False)
    
    def __str__(self):
        return self.fullname


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    dis = models.IntegerField(default=0)
    status = models.BooleanField(default=False) 
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return self.code


class Order(models.Model):
    STATUS = (
        ('Placed', 'Placed',),
        ('Canceled', 'Canceled'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
    )

    
    user = models.ForeignKey(Customer, on_delete=CASCADE)
    item = models.ForeignKey(Product, on_delete=CASCADE)
    order_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    price = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=CASCADE, null=True)
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    status = models.CharField(choices= STATUS, max_length=50, default='PLACED')
    pay_method = models.CharField(max_length=100, default='COD')
    coupon = models.ForeignKey(Coupon, on_delete=CASCADE, null=True)


    

    def __str__(self):
        return self.status


class Cart_count(models.Model):
    user = models.ForeignKey(Customer, on_delete=CASCADE)
    count = models.CharField(max_length=50)

    def __str__(self):
        return self.count
    

    
        

    





    
    


    
    


    
