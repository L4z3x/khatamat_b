from django.db import models
from khatma.models import khatmaGroup,Khatma
from api.models import MyUser
from django.utils import timezone
from community.models import community,post



class Notification(models.Model):
    STATUS = [
        ("read","read"),
        ("unread","unread"),
        ("pending","pending"),
        ("accepted","accepted"),
        ("rejected","rejected"),
    ]
    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False)
    status = models.CharField(max_length=10,choices=STATUS,default="unread")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class joinRequest(Notification):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False,related_name="incoming_join_req")
    community = models.ForeignKey(community,on_delete=models.CASCADE,null=True)    
    
    class Meta:
        unique_together =  [("user","community","owner")]
   
    def __str__(self):
        return f" R:from {self.user} to {self.owner} in {self.community}"


class messageN(Notification):
    # message = models.ForeignKey()
    khatmaGroup = models.ForeignKey(khatmaGroup,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message} in {self.khatmaGroup}'


class postN(Notification):
    post = models.ForeignKey(post,on_delete=models.CASCADE)
    community = models.ForeignKey(community,on_delete=models.CASCADE)    
    def __str__(self):
        return f'notification of {self.post.title}'
    

# class invitationN(Notification):
#     invitation = models.ForeignKey(invitation)

class brothershipRequest(Notification):
    brother = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='incoming_brothership_req')
    class Meta:
        unique_together = [("brother","owner")]

    def __str__(self):
        return f"{self.owner.username} to {self.brother.username}"
    