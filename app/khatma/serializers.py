from rest_framework import serializers
from khatma.models import Khatma,khatmaMembership


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

        
class khatma_membSerializer(serializers.ModelSerializer):
    class Meta:
        model = khatmaMembership
        fields = "__all__"
  
