from rest_framework import serializers
from .models import *

class joinRequestSerializer(serializers.Serializer): # c est pas comme ca aaah ???!!!
    G_name = serializers.CharField(max_length=40)



class brothershipReqSerialiazer(serializers.ModelSerializer):

    class Meta:
        model = brothershipRequest
        fields = ['brother','owner','status','created_at'] 

