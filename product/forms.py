from django import forms
from django.forms.models import inlineformset_factory
from .models import Product,ProductImage,ProductVariation,Brand

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'category', 'brand', 'description', 'image')
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        self.fields['category'].widget.attrs.update({'class':'form-select'})
        self.fields['image'].widget.attrs.update({'class':'form-control'})
        self.fields['brand'].widget.attrs.update({'class':'form-select'})
        self.fields['brand'].empty_label = 'Select Brand'
        self.fields['category'].empty_label = 'Select Category'
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({'class': 'form-control'})
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class':'form-control'})

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ('product','flavour', 'weight','price','quantity')

    def __init__(self, *args, **kwargs):
        super(ProductVariationForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class':'form-select'})
        self.fields['flavour'].widget.attrs.update({'class':'form-control'})
        self.fields['weight'].widget.attrs.update({'class':'form-control'})
        self.fields['price'].widget.attrs.update({'class':'form-control'})
        self.fields['quantity'].widget.attrs.update({'class':'form-control'})
        self.fields['product'].empty_label = "---Select Product---"


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('brand_name', 'brand_image', 'description')
    def __init__(self, *args, **kwargs):
        super(BrandForm,self).__init__(*args, **kwargs)
        self.fields['brand_name'].widget.attrs.update({'class':'form-control'})
        self.fields['brand_image'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        
