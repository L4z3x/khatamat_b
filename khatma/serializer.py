from rest_framework import serializers
from khatma.models import *


class khatmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khatma
        fields = '__all__'

class khatmaGroupDisplaySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(allow_empty_file=True,allow_null=True,required=False)
    class Meta:
        model = khatmaGroup
        fields = ["id","name","icon"]
    
class khatmaGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = khatmaGroup
        fields = '__all__' 
        
class groupSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = khatmaGroupSettings
        fields = "__all__"
 
class khatma_membSerializer(serializers.ModelSerializer):
    class Meta:
        model = khatmaMembership
        fields = "__all__"
    
class messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = ['id', 'group', 'sender', 'message', 'created_at','updated_at']