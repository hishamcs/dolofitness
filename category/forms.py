from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','description','category_image')
        widgets = {
            'category_name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'category_image':forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
