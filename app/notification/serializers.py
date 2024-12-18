from rest_framework import serializers
from .models import *


class brothershipReqSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = brothershipRequest
        fields = ['brother','owner','status','created_at'] 

