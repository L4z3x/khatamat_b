from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class MyUser(AbstractBaseUser, PermissionsMixin):
    Gender_list = [
        ('male', 'M'),
        ('female','F'),
    ]
    country_list=[
        ('Algeria','DZ'),
]
    # i think i am gonna add setting class
    username = models.CharField(unique=True,max_length=20)
    fullname = models.CharField(max_length=30,null=False)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True,max_length=254)
    gender = models.CharField(max_length=7,choices=Gender_list,default="M")
    country = models.CharField(max_length=20,choices=country_list,default="DZ")
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True,null=True)
    profilePic = models.ImageField(upload_to="UserPofilePic",default='UserProfilePic/default.png',null=False)
    khatmasNum = models.IntegerField(default=0)
    brothersNum = models.IntegerField(default=0)
    brothers = models.ManyToManyField('self',symmetrical=False, through='brothership',related_name='brothers_set')
    private = models.BooleanField(default=False,null=False)
    blocked = models.ManyToManyField('self',symmetrical=False,default=None) # to be rethinked with it's views

    objects = UserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def updateKhatmasNum(self,*args,**kwargs): # update khatma number seperately
        groupMem = self.groupMembership.all()
        self.khatmasNum = 0
        for g in groupMem:
            for kh in g.khatmaMembership.all():
                if kh.progress == 100 and kh.status == "completed": 
                    self.khatmasNum += 1
        super().save(*args,**kwargs)

    def __str__(self):
        return self.username


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