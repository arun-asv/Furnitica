from django.db import models
from django.db.models.deletion import CASCADE
from twilio.rest import Client
import random
from store.models import Product
import uuid


# Create your models here.

class Customer(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200) 
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=50)
    number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=100)
    
    
    

    def __str__(self):
        return self.firstname


class Otp(models.Model):
    num = models.IntegerField()
    validnum = random.randint(1000, 9999)
    vnum = validnum

    def __str__(self):
        return self.num




# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
    # def createotp(self):
    #     account_sid = 'ACff1e64ebbdeee1666cee5ab643b03f4e'
    #     auth_token = '75a5794ed0b273d45250f895de4018e6'
    #     client = Client(account_sid, auth_token)

    #     verification = client.verify \
    #                     .services('VAa72b019f75b36a4167324c9640c94ada') \
    #                     .verifications \
    #                     .create(to='+91'+str(self.num), channel='sms')

    #     print(verification.status)
    
    # def checkotp(self):
    #     account_sid = 'ACff1e64ebbdeee1666cee5ab643b03f4e'
    #     auth_token = '75a5794ed0b273d45250f895de4018e6'
    #     client = Client(account_sid, auth_token)

    #     verification_check = client.verify \
    #                        .services('VAa72b019f75b36a4167324c9640c94ada') \
    #                        .verification_checks \
    #                        .create(to='+91'+(self.num), code= self.vnum)

    #     print(verification_check.status)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    
    def sub_total(self):
        return self.product.price * self.quantity

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


class Order(models.Model):
    STATUS = (
        ('Placed', 'Placed',),
        ('Canceled', 'Canceled'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
    )

    
    user = models.ForeignKey(Customer, on_delete=CASCADE)
    item = models.ForeignKey(CartItem, on_delete=CASCADE)
    order_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    price = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=CASCADE, null=True)
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    status = models.CharField(choices= STATUS, max_length=50, default='PLACED')
    pay_method = models.CharField(max_length=100, default='COD')


    

    def __str__(self):
        return self.status

    

    
        

    





    
    


    
    


    
