from rest_framework import serializers
from .models import MyUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','username','email','password','gender','country','is_staff','is_superuser']
        extra_kwargs = {"password": {"write_only": True}}
