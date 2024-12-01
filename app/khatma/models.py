from django.db import models
from api.models import MyUser


class groupManager(models.Manager):
    def create_group(self,name,members=None,**extra):
        if not members:
            raise ValueError("expected members argument ??")
        group = self.create(name=name,**extra)
        group.members.set(members)
        return group

class group(models.Model):  
    name = models.CharField(max_length=40)
    icon = models.ImageField(upload_to="groupImages/",serialize=True)
    members = models.ManyToManyField(MyUser,through="groupMembership",related_name="group")
    description = models.CharField(max_length=290,default='BIO')    
    objects = groupManager()
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs) 
        # TODO: move this to signal.py 
        if not hasattr(self,"settings"):
            settings = groupSettings.objects.create(group=self)
            self.settings = settings
            self.settings.save()        
            
            
class groupSettings(models.Model): # settings related to khatma
    MemberChoices = [
        ("all","all"),
        ("only_admins","only_admins"),
        ("custom","custom"),
    ]

    # private = models.BooleanField(default=False,null=False)  i forgot why i added this field
    group = models.OneToOneField(group,on_delete=models.CASCADE,related_name="settings")
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
            
class groupMembership(models.Model): # users inside a khatma group
    ROLE = [
        ("admin","admin"),
        ("user","user"),
    ]
    since = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name="groupMembership")
    group = models.ForeignKey(group,on_delete=models.CASCADE,related_name="membership")
    role = models.CharField(default="admin",max_length=6,choices=ROLE,blank=False)
    def __str__(self):
        return f"{self.user} in {self.group} group"


class media(models.Model):
    file = models.FileField(upload_to=f"groupMedia/",null=True,serialize=True)
    
    def __str__(self) -> str:
        return f"{self.id}: {self.message.sender} -> {self.message}"


class message(models.Model):
    sender = models.ForeignKey(groupMembership,on_delete=models.CASCADE,related_name="sentMessages")
    group = models.ForeignKey(group,on_delete=models.CASCADE,related_name="messages")
    message = models.TextField(max_length=5000,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    removed = models.BooleanField(default=False)
    reply = models.ForeignKey("self",on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    file = models.OneToOneField(media,on_delete=models.CASCADE,related_name="message",null=True,blank=True)
    file_path = models.FilePathField(path="/app/files/groupMedia",null=True,blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["group", "created_at"]),
            models.Index(fields=["sender"]),
        ]
    def __str__(self):
        return f"{self.id}: {self.sender.user} : {self.group} : {self.message[:40]}"


# khatma section:
      
class KhatmaManager(models.Manager): # khatma model manager (create,delet,update,list)
    def create_khatma(self, name, group,period):
        if group:
            khatma = self.model(name=name,period=period,group=group)
            khatma.save()
            return khatma
        raise ValueError("expected group argument ??")

    def delete_khatma(self, name):
        khatma = self.get(name=name)
        khatma.delete(using=self._db)
        return khatma
    
    def list_khatma_member(self,name):
        khatma = self.get(name=name)
        return khatma.group.members.all()

SurahList = [
        ("the cow","the cow"),
     ]

KhatmaStatusList = [
        ("ongoing","ongoing"),
        ("completed","completed"),
        ("aborted","aborted"),
]

class Khatma(models.Model):    # khatma instance created by a group Admin
    
    launcher = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,related_name="launched_khatmas")  
    name = models.CharField(max_length=20,null=False)
    group = models.ForeignKey(group,on_delete=models.CASCADE,null=False,default=None)
    endDate = models.DateTimeField(null=False)
    intentions = models.CharField(max_length=180,default=None) # required , not null provide choices
    duaa = models.CharField(max_length=180,default=None) # required , not null provide choices
    startSurah = models.CharField(max_length=35,choices=SurahList)
    startVerse = models.PositiveIntegerField(null=False,default=0)
    endSurah = models.CharField(max_length=35,choices=SurahList) 
    endVerse = models.PositiveIntegerField(null=False,default=0)
    
    progress = models.PositiveIntegerField(default=0,null=False)
    status = models.CharField(choices=KhatmaStatusList,max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = KhatmaManager()
    
    class Meta:
        unique_together = [("name","group")]
        
    def __str__(self):
        return f"{self.name} in {self.group}"
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        total_membership = 0
        total_progress = 0
        for membership in khatmaMembership.objects.filter(khatma=self):
            total_progress += membership.progress
            total_membership += 1
        if total_membership != 0:
            self.progress = int(total_progress / total_membership)
            super().save(*args,**kwargs)
        
class khatmaMembership(models.Model):
    
    groupMembership = models.ForeignKey(groupMembership,on_delete=models.CASCADE,null=False,related_name="khatmaMembership")   
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
        unique_together = [("khatma","groupMembership")]
    
    def __str__(self):
        name = f"{self.groupMembership} in {self.khatma.name}" 
        return name

    def save(self,*args,**kwargs):            
        super().save()
