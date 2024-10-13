from rest_framework import serializers
from khatma.models import Khatma,khatmaMembership


class khatmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khatma
        fields = ["name","period"]
        

    