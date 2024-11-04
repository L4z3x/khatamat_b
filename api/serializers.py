from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'fullname', 'username', 'email', 'password', 'gender', 'country', 'profilePic',"date_joined"]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "fullname": {"required": False},
            "username": {"required": False},
            "email": {"required": False},
            "gender": {"required": False},
            "country": {"required": False},
            "profilePic": {"required": False},
        }

class brotherDataSer(serializers.Serializer):
    id = serializers.IntegerField()
    img = serializers.ImageField(source="profilePic")
    username = serializers.CharField(max_length=20)
    # since = serializers.DateTimeField() will be added in the view ;)
    class Meta:
        fields = ['img','username','since','id']