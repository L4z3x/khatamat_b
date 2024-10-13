from khatma.serializer import khatmaSerializer
from api.models import MyUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from khatma.models import Khatma,khatmaMembership
from rest_framework.permissions import IsAuthenticated
# Create your views here.


# create a khatma with one admin membership which is the sender
class CreateKhatma(views.APIView):   
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None): 
        seriliazer = khatmaSerializer(data=request.data)
        if seriliazer.is_valid():
            data = seriliazer.validated_data
            user = request.user
            khatma = Khatma.objects.create_khatma(name=data["name"],period=data["period"],member=[user])
            khatmaMembership.objects.create_khatmaMembership(user=user,khatma=khatma,role="admin")
            return Response(data=data,status=status.HTTP_201_CREATED)
        return Response(seriliazer.errors,status=status.HTTP_400_BAD_REQUEST)    

# add a member to a khatma (craete a user membership)
    

class getkhatma(views.APIView):
    def get(self,request,format=None):
        name = request.query_params.get("name")
        if name:
            try:
                khatma = Khatma.objects.get(name=name)   # check for khatma existence
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            khatma = khatmaSerializer(data = khatma)       # serialize data
            if khatma.is_valid():
                khatma = khatma.validated_data              # get data
                return Response(data=khatma,status=status.HTTP_200_OK)
            return Response({"error":"khatma not complete or empty"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"no name provided"},status=status.HTTP_400_BAD_REQUEST)

        
      
      
      
        # user = MyUser.objects.get(username=username)
        # khatma = Khatma.objects.create_khatma(name=name,period=period,member=user)
        # if khatma:    
        #     khatma.save()
        #     return Response("khatma created successfully",status=status.HTTP_201_CREATED)
        # else:
        #     return Response("failed to create khatma",status=status.HTTP_400_BAD_REQUEST)
