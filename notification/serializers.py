from rest_framework import serializers
from .models import *

class joinRequestSerializer(serializers.Serializer):
    G_name = serializers.CharField(max_length=40)


class brothershipSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class brothershipReqSerialiazer(serializers.ModelSerializer):

    class Meta:
        model = brothershipRequest
        fields = ['brother','owner','status','created_at'] 


class brothershipReqDataSer(serializers.Serializer):
    id = serializers.IntegerField()
    img = serializers.ImageField(source="profilePic")
    username = serializers.CharField(max_length=20)
    # since = serializers.DateTimeField() will be added in the view ;)
    class Meta:
        fields = ['img','username','since','id']