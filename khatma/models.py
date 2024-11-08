from django.db import models
from api.models import MyUser
from django.utils import timezone
from community.models import upload_to


class khatmaGroupManager(models.Manager):
    def create_khatmaGroup(self,name,members,**extra):
        if members:
            if extra:
                icon = extra[0]
                KG = self.model(name=name,icon=icon)
            else:
                KG = self.model(name=name)
            KG.save(using=self._db)
            # for i in members:
                # khatmaGroupMembership.objects.create(user=user)
            KG.members.set(members)
            return KG
        raise ValueError("expected members argument ??")

        
class KhatmaManager(models.Manager): # khatma model manager (create,delet,update,list)
    def create_khatma(self, name, khatmaGroup,period):
        if khatmaGroup:
            khatma = self.model(name=name,period=period,khatmaGroup=khatmaGroup)
            khatma.save()
            return khatma
        raise ValueError("expected khatmaGroup argument ??")

    def delete_khatma(self, name):
        khatma = self.get(name=name)
        khatma.delete(using=self._db)
        return khatma
    
    def list_khatma_member(self,name):
        khatma = self.get(name=name)
        return khatma.khatmaGroup.members.all()


class khatmaGroup(models.Model):
    name = models.CharField(max_length=40)
    icon = models.ImageField(upload_to=upload_to('khatmaGroupImage',f'{name}_{id}'),serialize=True)
    members = models.ManyToManyField(MyUser,through="khatmaGroupMembership",related_name="khatmaGroup")
    bio = models.CharField(max_length=290,default='BIO')    
    objects = khatmaGroupManager()

    def __str__(self):
        return self.name


class khatmaGroupMembership(models.Model):
    ROLE = [
        ("admin","admin"),
        ("user","user"),
    ]
    since = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    khatmaGroup = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE,related_name="khatma_G_membership")
    role = models.CharField(default="admin",max_length=6,choices=ROLE,blank=False)
    def __str__(self):
        return f"{self.user} in {self.khatmaGroup} group"


class Khatma(models.Model):    # khatma instance created by a khatmaGroup Admin
    
    # model Fields
    name = models.CharField(max_length=20,null=False)
    khatmaGroup = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE,null=False,default=None)
    startDate = models.DateTimeField(null=False)
    endDate = models.DateTimeField(null=False)#,default=timezone.datetime(2024, 10, 29, 10, 11, 45, 187116)) # required, not null
    intentions = models.CharField(max_length=180,default=None) # required , not null provide choices
    duaa = models.CharField(max_length=180,default=None) # required , not null provide choices

    class Meta:
        unique_together = [("name","khatmaGroup")]
    objects = KhatmaManager()
    def __str__(self):
        return f"{self.name} in {self.khatmaGroup}"


class khatmaMembership(models.Model):
    SurahList = [
        ("the Cow","the Cow"),
     ]
    khatmaGroupMembership = models.ForeignKey(khatmaGroupMembership,on_delete=models.CASCADE,null=False,default=None)   
    khatma = models.ForeignKey(Khatma,on_delete=models.CASCADE,null=False,default=None)
   
    startShareSurah = models.CharField(max_length=35,choices=SurahList,default="the Cow") # remove default
    startShareVerse = models.IntegerField(default=1) # remove default
    endShareSurah = models.CharField(max_length=35,choices=SurahList,default='the Cow') # remove default
    endShareVerse = models.IntegerField(default=280) # remove default

    class Meta:
        unique_together = [("khatma","khatmaGroupMembership")]
    def __str__(self):
        name = f"{self.khatmaGroupMembership} in {self.khatma.name}" 
        return name

class message(models.Model):
    sender = models.ForeignKey(khatmaGroupMembership,on_delete=models.CASCADE)
    group = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE)
    message = models.TextField(max_length=400000,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id}: {self.sender.user} : {self.group} : {self.message[:40]}"