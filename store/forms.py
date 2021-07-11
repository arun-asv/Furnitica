from customer.models import Coupon
from typing import AbstractSet
from django import forms
from .models import Category, Product   
from django.forms import ModelForm, widgets
from django.forms.fields import Field


class CategoryForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.FileInput,)
    class Meta:
        model = Category
        fields = ('cat_name', 'img')
    

    def __init__(self, *args, **kwargs):
        super (CategoryForm, self).__init__(*args, **kwargs)


        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

    


class ProductForm(forms.ModelForm):
    image1 = forms.ImageField(widget=forms.FileInput,)
    image2 = forms.ImageField(widget=forms.FileInput,)
    image3 = forms.ImageField(widget=forms.FileInput,)

    class Meta:
        model = Product
        fields = ('product_name', 'image1', 'image2', 'image3', 'category', 'price')

        widgets ={
            'category':forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super (ProductForm, self).__init__(*args, **kwargs)


        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'



