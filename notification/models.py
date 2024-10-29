from django.db import models
from khatma.models import khatmaGroup,Khatma
from api.models import MyUser
from django.utils import timezone



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