from rest_framework import generics,views
from django.shortcuts import get_object_or_404
from .models import MyUser,joinRequest
from rest_framework import status 
from rest_framework.response import Response
from .serializers import UserSerializer,joinRequestSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from khatma.models import khatmaGroupMembership,khatmaGroup
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

# tested and working >>> send multiple join requests to admins of a khatma group
class create_JoinRequest(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serailizer = joinRequestSerializer(data= request.data) 
        if serailizer.is_valid():
            user = request.user
            data = serailizer.validated_data
            try:
                khatmagroup = khatmaGroup.objects.get(name=data['G_name'])
            except:
                return Response(data={"error":"khatma group not found"},status=status.HTTP_404_NOT_FOUND)
            ownersMem = khatmagroup.khatma_G_membership.filter(role="admin")
            owners = ownersMem.values_list("user",flat=True)
            print(owners)
            admins =[]
            for i in owners:
                try:
                    owner = MyUser.objects.get(id=i)
                    join_req = joinRequest.objects.get(owner=owner,user=user,khatmaGroup=khatmagroup)
                except:
                    join_req = None
                if not join_req:
                    joinrequest = joinRequest.objects.create(owner=owner,user=user,khatmaGroup=khatmagroup)
                    joinrequest.save()
                    admins += joinrequest.owner.username
                else:
                    pass
                if not admins:
                    return Response(data={"msg":"requset already sent"},status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    return Response(data={"admins":f"{len(admins)}"},status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    