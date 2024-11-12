from django.db import models
from api.models import MyUser
from community.models import upload_to


class khatmaGroupManager(models.Manager):
    def create_khatmaGroup(self,name,members=None,**extra):
        if not members:
            raise ValueError("expected members argument ??")
        group = self.create(name=name,**extra)
        group.members.set(members)
        return group

  
class khatmaGroup(models.Model):  
    name = models.CharField(max_length=40)
    icon = models.ImageField(upload_to=upload_to('khatmaGroupImage',f'{name}_{id}'),serialize=True)
    members = models.ManyToManyField(MyUser,through="khatmaGroupMembership",related_name="khatmaGroup")
    description = models.CharField(max_length=290,default='BIO')    
    private = models.BooleanField(default=False,null=False)
    
    objects = khatmaGroupManager()
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if not hasattr(self,"settings"):
            settings = khatmaGroupSettings.objects.create(group=self)
            self.settings = settings
            self.settings.save()        
            
            
class khatmaGroupSettings(models.Model): # settings related to khatma
    MemberChoices = [
        ("all","all"),
        ("only_admins","only_admins"),
        ("custom","custom"),
    ]
    
    group = models.OneToOneField(khatmaGroup,on_delete=models.CASCADE,related_name="settings")
    canAddMember = models.CharField(max_length=12,default="all",choices=MemberChoices)
    canAddMember_custom = models.ManyToManyField(MyUser,related_name="canAddMember")
    canSendMessage = models.CharField(max_length=12,default="all",choices=MemberChoices)
    canSendMessage_custom = models.ManyToManyField(MyUser,related_name="canSendMessage")
    All_can_suggest_khatma = models.BooleanField(default=True,null=False)  
    
    def __str__(self):
        return f"{self.group.name} settings"
    
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)        
        for user in self.canSendMessage_custom.all():
            if not user in self.group.members.all():
                self.canSendMessage_custom.remove(user)
        for user in self.canAddMember_custom.all():
            if not user in self.group.members.all():
                self.canAddMember_custom.remove(user)
        
    
class khatmaGroupMembership(models.Model): # users inside a khatma group
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


class message(models.Model):
    sender = models.ForeignKey(khatmaGroupMembership,on_delete=models.CASCADE)
    group = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE)
    message = models.TextField(max_length=400000,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id}: {self.sender.user} : {self.group} : {self.message[:40]}"

# khatma section:

      
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


class Khatma(models.Model):    # khatma instance created by a khatmaGroup Admin
    
    # model Fields
    launcher = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,related_name="launched_khatmas")  
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
   
    startShareSurah = models.CharField(max_length=35,choices=SurahList)
    startShareVerse = models.IntegerField()
    endShareSurah = models.CharField(max_length=35,choices=SurahList) 
    endShareVerse = models.IntegerField() 

    class Meta:
        unique_together = [("khatma","khatmaGroupMembership")]
    def __str__(self):
        name = f"{self.khatmaGroupMembership} in {self.khatma.name}" 
        return name


