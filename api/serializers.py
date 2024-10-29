from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','username','email','password','gender','country']
        extra_kwargs = {"password": {"write_only": True}}

class joinRequestSerializer(serializers.Serializer):
    G_name = serializers.CharField(max_length=40)