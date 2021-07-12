from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import ModelChoiceField
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    cat_name = models.CharField(max_length=200)
    img = models.ImageField(upload_to = 'pics/profile')
    offer = models.IntegerField(default=0)

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    image1 = models.ImageField(upload_to = 'pics/products', blank=True)
    image2 = models.ImageField(upload_to = 'pics/products', blank=True)
    image3 = models.ImageField(upload_to = 'pics/products', blank=True)
    category = models.ForeignKey(Category, on_delete=CASCADE)
    price = models.IntegerField()
    offer = models.IntegerField(default=0)
    finalprice = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name
        