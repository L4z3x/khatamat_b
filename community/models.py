from django.db import models
from api.models import MyUser
from django.utils import timezone


class community (models.Model):
    name = models.CharField(max_length=20,null=False)
    members = models.ManyToManyField(MyUser,through="communityMembership")
    bio = models.TextField()

    def __str__(self):
        return self.name


class communityMembership(models.Model):
    user =  models.ForeignKey(MyUser,on_delete=models.CASCADE)
    community = models.ForeignKey(community,on_delete=models.CASCADE)
    role = models.CharField(max_length=10,null=False) 

    def __str__(self):
        return f'{self.user} in {self.community}'


def upload_to(folder,filename):
    return f'{folder}/{filename}'.format(filename=filename)


class post(models.Model):
    user = models.ForeignKey(communityMembership,on_delete=models.CASCADE)
    community = models.ForeignKey(community,on_delete=models.CASCADE)
    title = models.TextField(max_length=300,null=False)
    body = models.TextField(max_length=3000,null=False)
    status = models.CharField(max_length=10)
    views = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to=upload_to('postImg',f'{title}'))
    video = models.FileField(upload_to=upload_to('postVideo',f'{title}'))
    comment_n = models.IntegerField()
    
    def __str__(self):
        return self.title
    

class comment(models.Model):
    user = models.ForeignKey(communityMembership,on_delete=models.CASCADE)
    post = models.ManyToManyField(post)
    text = models.TextField(max_length=3000)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"

    @property
    def is_reply(self):
        return self.parent is not None