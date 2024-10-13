from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self,username,email,gender,country,password=None, **extra_fields):
        if not username or not email:
            raise ValueError('You Must Include a username and an email')
        email = self.normalize_email(email)
        extra_fields.setdefault('date_joined',timezone.now()) 
        user = self.model(username=username,email=email,gender=gender,country=country,**extra_fields)
        user.set_password(password)
        user.save(using=self._db) 
        return user
    def create_superuser(self,username,email,gender,country,password=None, **extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        return self.create_user(username,email,gender,country,password, **extra_fields)


class MyUser(AbstractBaseUser,PermissionsMixin):
    Gender_list = [
        ('male', 'M'),
        ('female','F'),
    ]
    country_list=[
        ('Algeria','DZ'),
        
    ]
    username = models.CharField(unique=True,max_length=20)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True,max_length=254)
    gender = models.CharField(max_length=7,choices=Gender_list,default=None)
    country = models.CharField(max_length=20,choices=country_list,default=None)
    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(blank=True,null=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'gender', 'country']
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
