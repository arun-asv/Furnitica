from django.contrib import admin
from . models import Address, CartItem, Customer, Otp

# Register your models here.
    
admin.site.register(Customer)
admin.site.register(Otp)
admin.site.register(Address)
admin.site.register(CartItem)
