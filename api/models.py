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
        user = self.model(username=username,email = email,gender=gender,country=country,**extra_fields)
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

        

class Part(models.Model):            # TODO: Add customization....

    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name= 'parts')
    part01 = models.CharField(max_length=20, blank=True, null=True)
    part02 = models.CharField(max_length=20, blank=True, null=True)
    part03 = models.CharField(max_length=20, blank=True, null=True)
    part04 = models.CharField(max_length=20, blank=True, null=True)
    part05 = models.CharField(max_length=20, blank=True, null=True)
    part06 = models.CharField(max_length=20, blank=True, null=True)
    part07 = models.CharField(max_length=20, blank=True, null=True)
    part08 = models.CharField(max_length=20, blank=True, null=True)
    part09 = models.CharField(max_length=20, blank=True, null=True)
    part10 = models.CharField(max_length=20, blank=True, null=True)
    part11 = models.CharField(max_length=20, blank=True, null=True)
    part12 = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        part_fields = [
            self.part01, self.part02, self.part03, self.part04,
            self.part05, self.part06, self.part07, self.part08,
            self.part09, self.part10, self.part11, self.part12
        ]
        non_empty_count = sum(1 for part in part_fields if part)  # count the non-empty fields
        return f"{self.user.username}={non_empty_count}"