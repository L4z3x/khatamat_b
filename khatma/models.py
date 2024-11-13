from django.db import models
from api.models import MyUser


class khatmaGroupManager(models.Manager):
    def create_khatmaGroup(self,name,members=None,**extra):
        if not members:
            raise ValueError("expected members argument ??")
        group = self.create(name=name,**extra)
        group.members.set(members)
        return group

class khatmaGroup(models.Model):  
    name = models.CharField(max_length=40)
    icon = models.ImageField(upload_to="khatmaGroupImages/",serialize=True)
    members = models.ManyToManyField(MyUser,through="khatmaGroupMembership",related_name="khatmaGroup")
    description = models.CharField(max_length=290,default='BIO')    
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

    # private = models.BooleanField(default=False,null=False)  i forgot why i added this field
    group = models.OneToOneField(khatmaGroup,on_delete=models.CASCADE,related_name="settings")
    canAddMember = models.CharField(max_length=12,default="all",choices=MemberChoices)
    canAddMember_custom = models.ManyToManyField(MyUser,related_name="canAddMember")
    canSendMessage = models.CharField(max_length=12,default="all",choices=MemberChoices)
    canSendMessage_custom = models.ManyToManyField(MyUser,related_name="canSendMessage")
    All_can_launch_khatma = models.BooleanField(default=True,null=False)  
    
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
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name="khatmaGroupMembership")
    khatmaGroup = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE,related_name="khatma_G_membership")
    role = models.CharField(default="admin",max_length=6,choices=ROLE,blank=False)
    def __str__(self):
        return f"{self.user} in {self.khatmaGroup} group"


class media(models.Model):
    group = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE,related_name="media")
    sender = models.ForeignKey(khatmaGroupMembership,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(upload_to="khatmaGroupMedia/")
    
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

SurahList = [
        ("the cow","the cow"),
     ]

KhatmaStatusList = [
        ("ongoing","ongoing"),
        ("completed","completed"),
        ("aborted","aborted"),
]

class Khatma(models.Model):    # khatma instance created by a khatmaGroup Admin
    
    launcher = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,related_name="launched_khatmas")  
    name = models.CharField(max_length=20,null=False)
    khatmaGroup = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE,null=False,default=None)
    endDate = models.DateTimeField(null=False)
    intentions = models.CharField(max_length=180,default=None) # required , not null provide choices
    duaa = models.CharField(max_length=180,default=None) # required , not null provide choices
    startSurah = models.CharField(max_length=35,choices=SurahList)
    startVerse = models.PositiveIntegerField(null=False,default=0)
    endSurah = models.CharField(max_length=35,choices=SurahList) 
    endVerse = models.PositiveIntegerField(null=False,default=0)
    
    progress = models.PositiveIntegerField(default=0,null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = KhatmaManager()
    
    class Meta:
        unique_together = [("name","khatmaGroup")]
        
    def __str__(self):
        return f"{self.name} in {self.khatmaGroup}"
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        total_membership = 0
        total_progress = 0
        for membership in khatmaMembership.objects.filter(khatma=self):
            total_progress += membership.progress
            total_membership += 1
        self.progress = total_progress / total_membership
        super().save(*args,**kwargs)
        
class khatmaMembership(models.Model):
    
    khatmaGroupMembership = models.ForeignKey(khatmaGroupMembership,on_delete=models.CASCADE,null=False,related_name="khatmaMembership")   
    khatma = models.ForeignKey(Khatma,on_delete=models.CASCADE,null=False,default=None)
   
    startShareSurah = models.CharField(max_length=35,choices=SurahList)
    startShareVerse = models.PositiveIntegerField(null=False,default=0)
    endShareSurah = models.CharField(max_length=35,choices=SurahList) 
    endShareVerse = models.PositiveIntegerField(null=False,default=0) 
    currentSurah = models.CharField(max_length=35,choices=SurahList)
    currentVerse = models.PositiveIntegerField(null=False,default=0)
    
    progress = models.PositiveIntegerField(default=0,null=False)
    
    finishDate = models.DateTimeField(null=True)
    status = models.CharField(max_length=20,default="ongoing",choices=KhatmaStatusList)
    
    class Meta:
        unique_together = [("khatma","khatmaGroupMembership")]
    
    def __str__(self):
        name = f"{self.khatmaGroupMembership} in {self.khatma.name}" 
        return name

    def save(self,*args,**kwargs):            
        super().save()
