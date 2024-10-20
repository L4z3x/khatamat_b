from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password


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


from khatma.models import khatmaGroup,Khatma

class Notification(models.Model):
    TYPES= [
        ("join request","join request"),
    ]
    STATUS = [
        ("read","read"),
         ("unread","unread")
    ]

    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False,related_name="notification_from")
    user = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,default=None,related_name="notification_to")
    kh_G = models.ForeignKey(khatmaGroup,on_delete=models.SET_NULL,null=True,default=None)
    Kh = models.ForeignKey(Khatma,on_delete=models.SET_NULL,null=True,default=None)
    type = models.CharField(max_length=100,choices=TYPES)
    message = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=10,choices=STATUS)
    created_at = models.DateTimeField(timezone.now)


    def __str__(self):
        return f"N:{self.type} for {self.owner}"


class joinRequest(models.Model):
    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False,related_name="JoinRequest_owner")
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False)
    khatmaGroup = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE,null=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together =  [("user","khatmaGroup","owner")]
    def __str__(self):
        return f" R:from {self.user} to {self.owner} in {self.khatmaGroup}"