from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,UserAddress,UserProfileImage, Wallet

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email','username','phone_number','is_active','last_login')
    readonly_fields = ('last_login','date_joined')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','profile_pic')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','first_name','last_name','email','address_line1','address_line2','phone','city','state','country','postcode','default_addr')

admin.site.register(Account,AccountAdmin)
admin.site.register(UserAddress,AddressAdmin)
admin.site.register(UserProfileImage)
admin.site.register(Wallet)