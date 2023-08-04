from django import forms
from .models import Account,UserAddress,UserProfileImage
import re
from django.contrib.auth.password_validation import validate_password

class RegistraionForm(forms.ModelForm):
    password            = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password    = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model   = Account
        fields  = ['username','email','phone_number','password']

    def __init__(self,*args, **kwargs):
        super(RegistraionForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'

    def clean(self):
        cleaned_data = super(RegistraionForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        error_msg_password = []
        if password != confirm_password:
            error_msg_password.append('Passwords do not match')
        if len(password) < 8:
            error_msg_password.append('Password should be at least 8 characters long')
        if not re.search(r'[A-Z]',password):
            error_msg_password.append('Password should contain at least one uppercase letter')
        if not re.search(r'[a-z]',password):
            error_msg_password.append('Password should contain atleast one lowercase letter')
        if not re.search(r'[0-9]',password):
            error_msg_password.append('Password should contain atleast one digit')
        if not re.search(r'[@#$%^&+=]',password):
            error_msg_password.append('Password should contain at least one special character (@#$%^&+=)')
        if error_msg_password:
            self.add_error('password',error_msg_password)
        
        phone_number = cleaned_data.get('phone_number')
        # phone_number_with_ctry_code = '+91'+phone_number
        if not re.match(r'^[0-9]+$', phone_number):
            self.add_error('phone_number', 'Phone number should contain only digits')
        if len(phone_number) < 10:
            self.add_error('phone_number','Please provide valid Phone number')
        # if Account.objects.filter(phone_number=phone_number_with_ctry_code).exists():
        #     self.add_error('phone_number','Account with this Phone number already exists.')



class UserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False,error_messages={'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        model  = UserProfileImage
        fields = ('first_name','last_name','profile_pic')

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username','phone_number', 'email')






class AddressForm(forms.ModelForm):
    class Meta:
        model   = UserAddress
        exclude = ['user','default_addr']


        
        
        