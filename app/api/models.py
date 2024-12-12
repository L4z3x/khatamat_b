from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class MyUser(AbstractBaseUser, PermissionsMixin):
 
    username = models.CharField(unique=True,max_length=20)
    email = models.EmailField(unique=True,max_length=254)
    profilePic = models.ImageField(upload_to="UserPofilePic",default='UserProfilePic/default.png',null=False)
    is_staff = models.BooleanField(default=False)
    brothers = models.ManyToManyField('self',symmetrical=False, through='brothership',related_name='brothers_set')
    blocked = models.ManyToManyField('self',symmetrical=False,default=None)
    muted_groups = models.ManyToManyField('khatma.group',default=None,related_name='muting_members')
    muted_brothers = models.ManyToManyField('self',symmetrical=False,default=None,related_name='muting_brothers')
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
   
    def __str__(self):
        return self.username
    
class UserSetting(models.Model):
    Gender_list = [
            ('male', 'M'),
            ('female','F'),
    ]
    country_list=[
            ('Algeria','DZ'),
    ]
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE,related_name='setting')  
    fullname = models.CharField(max_length=30,null=True)
    is_active = models.BooleanField(default= True)
    gender = models.CharField(max_length=7,choices=Gender_list,null=True,default=None)
    country = models.CharField(max_length=20,choices=country_list,null=True,default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True,null=True)
    khatmasNum = models.IntegerField(default=0)
    brothersNum = models.IntegerField(default=0)
    private = models.BooleanField(default=False,null=False)
    mode = models.CharField(max_length=20,default="light",choices=[("light","light"),("dark","dark")])
    
    def updateKhatmasNum(self,*args,**kwargs): # update khatma number seperately
        groupMem = self.groupMembership.all()
        self.khatmasNum = 0
        for g in groupMem:
            for kh in g.khatmaMembership.all():
                if kh.progress == 100 and kh.status == "completed": 
                    self.khatmasNum += 1
        super().save(*args,**kwargs)



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
        # self.clean()
        super().save(*args, **kwargs)
        
    
    
    def delete(self, *args, **kwargs):
        brothership.objects.filter(user1=self.user2, user2=self.user1).delete()
        super().delete(*args,**kwargs)