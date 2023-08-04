from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser


# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self,email,username,phone_number,password=None):
        if not email:
            raise ValueError('user muset have an email address')
        if not username:
            raise ValueError('user must have an user name')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,phone_number,password):
        user = self.create_user(email=email,username=username,phone_number=phone_number,password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    email           = models.EmailField(max_length=60,unique=True)
    username        = models.CharField(max_length=30)
    phone_number    = models.CharField(max_length=10,unique=True)

    is_active       = models.BooleanField(default=True)
    is_blocked      = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','phone_number']
    objects = AccountManager()

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_staff
    def has_module_perms(self,add_label):
        return True




class UserProfileImage(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField(blank=True,upload_to='userimage/',null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class UserAddress(models.Model):
    user            = models.ForeignKey(Account,on_delete=models.CASCADE)
    first_name      = models.CharField(max_length=20)
    last_name       = models.CharField(max_length=20)
    email           = models.EmailField(max_length=90)
    address_line1   = models.CharField(max_length=90)
    address_line2   = models.CharField(max_length=90)
    phone           = models.CharField(max_length=20)
    city            = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    country         = models.CharField(max_length=50)
    postcode        = models.CharField(max_length=15)
    default_addr    = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'
        

class Wallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username
    
    

    
               
    

