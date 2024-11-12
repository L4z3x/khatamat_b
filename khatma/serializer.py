from rest_framework import serializers
from khatma.models import *


class khatmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khatma
        fields = '__all__'

class khatmaGroupSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(allow_empty_file=True,allow_null=True,required=False)
    class Meta:
        model = khatmaGroup
        fields = ["id","name","icon"]
    

class khatma_membSerializer(serializers.ModelSerializer):
    class Meta:
        model = khatmaMembership
        fields = "__all__"
    
class messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = ['id', 'group', 'sender', 'message', 'created_at','updated_at']