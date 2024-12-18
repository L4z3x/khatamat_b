from django.db import models
from api.models import MyUser
from group.models import group,groupMembership,Code
      
      
      
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


class khatmaCode(Code):
    khatma = models.ForeignKey(Khatma,on_delete=models.CASCADE,related_name="links")
    issued_by = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name="issued_khatma_codes")