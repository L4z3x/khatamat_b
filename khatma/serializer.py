from rest_framework import serializers
from khatma.models import Khatma,khatmaGroup


class khatmaSerializer(serializers.ModelSerializer):
    G_name = serializers.CharField(max_length=40)
    class Meta:
        model = Khatma
        fields = ["name","period","G_name"]


class khatmaGroupSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(allow_empty_file=True,allow_null=True,required=False)
    class Meta:
        model = khatmaGroup
        fields = ["name","icon"]
    

class khatma_G_membSeriailizer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    G_name = serializers.CharField(max_length=40)



class khatma_membSerializer(serializers.Serializer):
    KH_name = serializers.CharField(max_length=20)
    G_name = serializers.CharField(max_length=40)
    