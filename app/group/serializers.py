from rest_framework import serializers
from .models import group,groupSettings,media,message,groupCode


class groupCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = groupCode
        fields = "__all__"
        extra_kwargs = {'group': {'required': False},
                        'issued_by': {'required': False},
                        'expiration_date': {'required': False},
                        'active': {'required': False},
                        'created_at': {'required': False},
                        'updated_at': {'required': False},
                        'code': {'required': False}}


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
        
    
class mediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = media
        fields = ["file","image","id"]
    
               
class   messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'
        
        