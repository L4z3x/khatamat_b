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

class Khatma(models.Model):
    duration_list=[
        ('1 day',1),
        ('2 day',2),
        ('3 day',3),
        ('4 day',4),
        ('5 day',5),
        ('6 day',6),
        ('week',7),
    ]
    hizbs_translated = [
        ("From 'Opener' verse 1 to 'Cow' verse 74", 1),
        ("From 'Cow' verse 75 to 'Cow' verse 141", 2),
        ("From 'Cow' verse 142 to 'Cow' verse 202", 3),
        ("From 'Cow' verse 203 to 'Cow' verse 252", 4),
        ("From 'Cow' verse 253 to 'Family of Imran' verse 14", 5),
        ("From 'Family of Imran' verse 15 to 'Family of Imran' verse 92", 6),
        ("From 'Family of Imran' verse 93 to 'Family of Imran' verse 170", 7),
        ("From 'Family of Imran' verse 171 to 'Women' verse 23", 8),
        ("From 'Women' verse 24 to 'Women' verse 87", 9),
        ("From 'Women' verse 88 to 'Women' verse 147", 10),
        ("From 'Women' verse 148 to 'The Table Spread' verse 26", 11),
        ("From 'The Table Spread' verse 27 to 'The Table Spread' verse 82", 12),
        ("From 'The Table Spread' verse 83 to 'Cattle' verse 35", 13),
        ("From 'Cattle' verse 36 to 'Cattle' verse 110", 14),
        ("From 'Cattle' verse 111 to 'Cattle' verse 165", 15),
        ("From 'The Heights' verse 1 to 'The Heights' verse 87", 16),
        ("From 'The Heights' verse 88 to 'The Heights' verse 170", 17),
        ("From 'The Heights' verse 171 to 'The Spoils of War' verse 40", 18),
        ("From 'The Spoils of War' verse 41 to 'Repentance' verse 33", 19),
        ("From 'Repentance' verse 34 to 'Repentance' verse 92", 20),
        ("From 'Repentance' verse 93 to 'Jonah' verse 25", 21),
        ("From 'Jonah' verse 26 to 'Hud' verse 5", 22),
        ("From 'Hud' verse 6 to 'Hud' verse 83", 23),
        ("From 'Hud' verse 84 to 'Joseph' verse 52", 24),
        ("From 'Joseph' verse 53 to 'Thunder' verse 18", 25),
        ("From 'Thunder' verse 19 to 'Abraham' verse 52", 26),
        ("From 'The Rocky Tract' verse 1 to 'The Bee' verse 50", 27),
        ("From 'The Bee' verse 51 to 'The Bee' verse 128", 28),
        ("From 'The Night Journey' verse 1 to 'The Night Journey' verse 98", 29),
        ("From 'The Night Journey' verse 99 to 'The Cave' verse 74", 30),
        ("From 'The Cave' verse 75 to 'Mary' verse 98", 31),
        ("From 'Ta-Ha' verse 1 to 'Ta-Ha' verse 135", 32),
        ("From 'The Prophets' verse 1 to 'The Prophets' verse 112", 33),
        ("From 'The Pilgrimage' verse 1 to 'The Pilgrimage' verse 78", 34),
        ("From 'The Believers' verse 1 to 'Light' verse 20", 35),
        ("From 'Light' verse 21 to 'The Criterion' verse 20", 36),
        ("From 'The Criterion' verse 21 to 'The Poets' verse 110", 37),
        ("From 'The Poets' verse 111 to 'The Ant' verse 55", 38),
        ("From 'The Ant' verse 56 to 'The Stories' verse 50", 39),
        ("From 'The Stories' verse 51 to 'The Spider' verse 45", 40),
        ("From 'The Spider' verse 46 to 'Luqman' verse 21", 41),
        ("From 'Luqman' verse 22 to 'The Confederates' verse 30", 42),
        ("From 'The Confederates' verse 31 to 'Sheba' verse 23", 43),
        ("From 'Sheba' verse 24 to 'Ya-Sin' verse 27", 44),
        ("From 'Ya-Sin' verse 28 to 'Those who set the Ranks' verse 144", 45),
        ("From 'Those who set the Ranks' verse 145 to 'The Groups' verse 31", 46),
        ("From 'The Groups' verse 32 to 'The Forgiver' verse 40", 47),
        ("From 'The Forgiver' verse 41 to 'Explained in Detail' verse 46", 48),
        ("From 'Explained in Detail' verse 47 to 'Ornaments of Gold' verse 23", 49),
        ("From 'Ornaments of Gold' verse 24 to 'The Crouching' verse 37", 50),
        ("From 'The Wind-Curved Sandhills' verse 1 to 'Victory' verse 17", 51),
        ("From 'Victory' verse 18 to 'The Winnowing Winds' verse 31", 52),
        ("From 'The Winnowing Winds' verse 32 to 'The Moon' verse 55", 53),
        ("From 'The Beneficent' verse 1 to 'Iron' verse 29", 54),
        ("From 'The Pleading Woman' verse 1 to 'The Hypocrites' verse 14", 55),
        ("From 'The Gathering' verse 1 to 'The Ranks' verse 12", 56),
        ("From 'The Sovereignty' verse 1 to 'Noah' verse 28", 57),
        ("From 'The Jinn' verse 1 to 'The Emissaries' verse 50", 58),
        ("From 'The Tidings' verse 1 to 'The Overwhelming' verse 17", 59),
        ("From 'The Most High' verse 1 to 'The Humanity' verse 6", 60)
    ]


    admin = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name='khatma')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="khatma_imgs")
    num_mem = models.IntegerField()  
    num_days = models.CharField(choices=duration_list,default=None)
    hizbs = models.CharField(choices=hizbs_list,defaul=None)    
    member = models.ManyToManyField(MyUser)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):  # add restriction ...
        if self.num_mem <= 1:
            return(error)
        if self.num_days > 7:
            self.num_days = 7
        super().save(**args, **kwargs)