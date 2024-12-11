from rest_framework import serializers
from .models import MyUser,UserSetting

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','username', 'email', 'password', 'profilePic']
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "username": {"required": False},
            "email": {"required": False},
            "profilePic": {"required": False},
        }
        

class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = ['id','user','fullname', 'gender','country','date_joined','brothersNum','private','khatmasNum','mode']
        extra_kwargs = {
            "user":{"read_only": True},
            "date_joined":{"read_only": True},
            "brothersNum":{"read_only": True},
            "brothers":{"read_only": True},
            "blocked":{"read_only": True},
            "khatmasNum":{"read_only": True},
        }

class brotherDataSer(serializers.Serializer):
    id = serializers.IntegerField()
    img = serializers.ImageField(source="profilePic")
    username = serializers.CharField(max_length=20)
    class Meta:
        fields = ['img','username','since','id']