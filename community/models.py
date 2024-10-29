from django.db import models
from api.models import MyUser
from django.utils import timezone
class community (models.Model):
    name = models.CharField(max_length=20,null=False)
    members = models.ManyToManyField(MyUser,through="communityMembership")

    def __str__(self):
        return self.name


class communityMembership(models.Model):
    user =  models.ForeignKey(MyUser,on_delete=models.CASCADE)
    community = models.ForeignKey(community,on_delete=models.CASCADE)
    role = models.CharField(max_length=10,null=False) 

    def __str__(self):
        return f'{self.user} in {self.community}'


def upload_to(instance, filename,folder):
    return f'{folder}/{filename}'.format(filename=filename)


class post(models.Model):
    user = models.ForeignKey(communityMembership)
    community = models.ForeignKey(community)
    title = models.CharField(max_length=300,null=False)
    body = models.CharField(max_length=3000,null=False)
    status = models.CharField(max_length=10)
    views = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to=upload_to('postImg'))
    video = models.FileField(upload_to=upload_to('postVideo'))
    
    def __str__(self):
        return self.title
    
    