from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from myapp.models import *

class checkoutform(forms.ModelForm):
    class Meta:
        model = order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email','paymentcardno']

class contactForm(ModelForm):
    class Meta:
        model = contact
        fields = ('name','surname','email','message')

class customerregistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = customer
        fields = ['username','password','name','surname','email','address']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Customer with this useername already exists")
             
        return username

class customerloginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Watch
        fields = ["brand", "model", "category", 'des',"image", "price",
                  ]
        widgets = {
            "brand": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "model": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the unique model here..."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "des": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the description title here..."
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Marked price of the product..."
            }),
            
        }


