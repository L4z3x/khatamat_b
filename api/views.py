
from rest_framework import generics
from django.http import HttpResponse
from .models import MyUser
from rest_framework import status 
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication,TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Create your views here.

class Userapi(generics.CreateAPIView, generics.ListAPIView,generics.UpdateAPIView,
    generics.RetrieveAPIView,generics.DestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
   # authentication_classes=[TokenAuthentication]
    #permission_classes = [IsAuthenticated,IsAdminUser]
    lookup_field = 'id'
    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    def post(self,request):
        return self.create(request)
    def put(self,request,id = None):
        return self.partial_update(request,id)
    def delete(self,request,id = None):
        if id:
            return self.destroy(request,id)
        else:
            return Response('No id specified',status=status.HTTP_400_BAD_REQUEST)
