from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:

        model = Address

        fields = ('fullname', 'email', 'address1', 'address2', 'mobile', 'pincode', 'landmark', 'country', 'check')

    def __init__(self, *args, **kwargs):
        super (AddressForm, self).__init__(*args, **kwargs)


        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'
