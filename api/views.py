
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import MyUser
from rest_framework import status 
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authtoken.models import Token
# Create your views here.


class ListUserapi(generics.ListAPIView,generics.RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)


class CreateUserapi(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        return self.create(request)


class UpdateUserapi(generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def put(self,request,id = None):
        return self.partial_update(request,id)

class DeleteUserapi(generics.DestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def delete(self,request,id = None):
        if id:
            return self.destroy(request,id)
        else:
            return Response('No id specified',status=status.HTTP_400_BAD_REQUEST)
