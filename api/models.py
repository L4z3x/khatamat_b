from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from func import upload_to


class MyUserManager(BaseUserManager):
    def create_user(self,username,email,gender,country,password=None, **extra_fields):
        if not username or not email:
            raise ValueError('You Must Include a username and an email')
        email = self.normalize_email(email)
        extra_fields.setdefault('date_joined',timezone.now()) 
        user = self.model(username=username,email=email,gender=gender,country=country,**extra_fields)
        user.set_password(password)
        for key, value in extra_fields.items():
            setattr(user, key, value)
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
    fullname = models.CharField(max_length=30,null=False)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True,max_length=254)
    gender = models.CharField(max_length=7,choices=Gender_list,default=None)
    country = models.CharField(max_length=20,choices=country_list,default=None)
    date_joined = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(blank=True,null=True)
    profilePic = models.ImageField(upload_to=upload_to(f'{username}','profilePic'),default='<django.db.models.fields.CharField>/profilePic/default.png',null=True)
    khatmasNum = models.IntegerField(default=0)
    brothersNum = models.IntegerField(default=0)
    brothers = models.ManyToManyField('self',symmetrical=True, through='brothership')

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'gender', 'country']

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username

    # def get_brothers(req,rec):
    #     try:
    #         bro = brothership.objects.get(user1=req,user2=rec)
    #         bro.is_active = True
    #         bro.save()
    #     except:
    #         raise ValueError("brothership not found")
    #     return bro


class brothership(models.Model):    
    user1 = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='brothership_initiated')
    user2 = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='brothership_received')
    brother_since = models.DateTimeField(default=timezone.now)


    class Meta:
        unique_together= ('user1','user2')
        verbose_name = 'Brothership'

    def __str__(self):
        return f'{self.user1.username} : {self.user2.username}'

    def clean(self): # custom def for checking the brothership
        if brothership.objects.filter(user1=self.user2, user2=self.user1).exists():
            raise ValueError("This brothership already exists in reverse.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)