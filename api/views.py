from rest_framework import generics,views
from .models import MyUser,brothership
from rest_framework import status 
from .serializers import *
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated,AllowAny

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
            return Response('No id specified',status=status. HTTP_400_BAD_REQUEST)

