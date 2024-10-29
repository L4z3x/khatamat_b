from django.db import models
from khatma.models import khatmaGroup,Khatma
from api.models import MyUser
from django.utils import timezone
from community.models import community



class Notification(models.Model):
    STATUS = [
        ("read","read"),
         ("unread","unread")
    ]
    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False,related_name="notification")
    status = models.CharField(max_length=10,choices=STATUS)
    created_at = models.DateTimeField(timezone.now)

    class Meta:
        abstract = True


class joinRequest(Notification):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False,related_name="JoinRequest_owner")
    community = models.ForeignKey(community,on_delete=models.CASCADE,null=False)    
    
    class Meta:
        unique_together =  [("user","community","owner")]
   
    def __str__(self):
        return f" R:from {self.user} to {self.owner} in {self.community}"


class message(Notification):
    # message = models.ForeignKey()
    khatmaGroup = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message} in {self.khatmaGroup}'


class postN(Notification):
    post = models.OneToOneField('joinRequest')
    
    def __str__(self) -> str:
        return f'notification of {self.post}'
    

# class invitationN(Notification):
#     invitation = models.ForeignKey(invitation)