from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','fullname','username','email','password','gender','country','profilePic']
        extra_kwargs = {"password": {"write_only": True}}

