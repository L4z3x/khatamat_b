from rest_framework import serializers
from khatma.models import *


class khatmaDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Khatma
        fields = ["name","progress","endDate","id"]


class khatmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khatma
        fields = '__all__'
        extra_kwargs = {'launcher': {'required': False},
                        'status': {'required': False},
                        'progress': {'required': False},
                        'endDate': {'required': False},
                        'intentions': {'required': False},
                        'duaa': {'required': False},
                        'startSurah': {'required': False},
                        'startVerse': {'required': False},
                        'endSurah': {'required': False},
                        'endVerse': {'required': False},
        }


class groupDisplaySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(allow_empty_file=True,allow_null=True,required=False)
    class Meta:
        model = group   
        fields = ["id","name","icon"]
    
    
class groupSerializer(serializers.ModelSerializer):
    class Meta:
        model = group
        fields = '__all__' 
        extra_kwargs = {'members': {'required': False},
                        'icon': {'required': False}}
 
        
class groupSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = groupSettings
        fields = "__all__"
    
        
class khatma_membSerializer(serializers.ModelSerializer):
    class Meta:
        model = khatmaMembership
        fields = "__all__"
  
  
class mediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = media
        fields = ["file","image","id"]
    
               
class   messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'
        
        
        
        