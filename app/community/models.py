from django.db import models
from api.models import MyUser
from django.utils import timezone



class communityManager(models.Manager):

    def create(self,admin,name,**extra):
        if admin:
            com = self.model(name=name)
            for key, value in extra.items():
                setattr(com, key, value)
            com.save(using=self._db)
        return com
    def update(self,id,**extra):
        try:
            com = community.objects.get(id=id)
        except Exception as e:
            return ValueError('community with this id cannot be found !')
        for key, value in extra.items():
            setattr(com, key, value)
        com.save()
        return com
    
    def delete(self,id):
        try:
            com = community.objects.get(id=id)
        except Exception as e:
            return ValueError('community with this id cannot be found !')
        com.delete()
        return 
    
    def retreive(self,id):
        try:
            com = community.objects.get(id=id)
        except Exception as e:
            raise ValueError('community with this id cannot be found !')
        return com

authenticationsList = [
    ("none","none"),
    ("custom","custom"),
]
class community (models.Model):
    name = models.CharField(max_length=20,null=False,unique=True)
    members = models.ManyToManyField(MyUser,through="communityMembership")
    authentications = models.CharField(max_length=20,choices=authenticationsList, default="none")
    picture = models.ImageField(upload_to="communityPic",null=True)
    bio = models.TextField(null=True)

    objects = communityManager()
    def __str__(self):
        return self.name

ROLE = [
        ("admin","admin"),
        ("user","user"),
    ]

class communityMembership(models.Model):
    user =  models.ForeignKey(MyUser,on_delete=models.CASCADE)
    community = models.ForeignKey(community,on_delete=models.CASCADE,related_name="membership")
    role = models.CharField(max_length=10,null=False,choices=ROLE) 

    def __str__(self):
        return f'{self.user} in {self.community}'


class post(models.Model):
    user = models.ForeignKey(communityMembership,on_delete=models.CASCADE)
    community = models.ForeignKey(community,on_delete=models.CASCADE)
    title = models.TextField(max_length=300,null=False)
    body = models.TextField(max_length=3000,null=False)
    status = models.CharField(max_length=10)
    views = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to="postPic")
    video = models.FileField(upload_to="postVid")
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