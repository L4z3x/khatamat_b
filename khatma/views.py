from khatma.serializer import khatmaSerializer,khatmaGroupSerializer,khatma_G_membSeriailizer, khatma_membSerializer
from api.models import joinRequest,Notification,MyUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from khatma.models import Khatma,khatmaMembership,khatmaGroupMembership,khatmaGroup
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser,MultiPartParser
from django.core.files import File
# Create your views here.


# create a khatmaGroup with one admin group membership which is the sender
class CreateKhatmaGroup(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self,request,format=None):
        serializer = khatmaGroupSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            data = serializer.validated_data
            khatma_group = khatmaGroup.objects.create_khatmaGroup(name=data['name'],members=[user])
            khatma_group.save()
            if "icon" in data.keys():
                khatma_group.icon.save("img2",data['icon']) # search about media folder and some stuff abt image field
                khatma_group.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# create a view that handles adding reglar users to khatma and another to a khatma group
#  (creating memberships)
class khatma_G_memb(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None): # add member to khatma group
        serializer = khatma_G_membSeriailizer(data=request.data)  # admin(sender), khatmaGroup,user
        
        if serializer.is_valid():
            data = serializer.validated_data
            admin = request.user
            khatmagroup = khatmaGroup.objects.get(name=data['G_name']) # retrieving katmaGroup
            
            if khatmagroup and admin:
                KGM_admin = khatmaGroupMembership.objects.get(role="admin",user=admin,khatmaGroup=khatmagroup) # checking admin
                if KGM_admin: 
                    user = MyUser.objects.get(username=data['username'])
                    join_req = joinRequest.objects.get(user=user,owner=admin,khatmaGroup=khatmagroup)
                    try:
                        KGM_member = khatmaGroupMembership.objects.get(user=user,khatmaGroup=khatmagroup)
                    except:
                        KGM_member = None
                    if not KGM_member:
                        if join_req and user :
                            new_kgm = khatmaGroupMembership.objects.create(user=user,role="user",khatmaGroup=khatmagroup)
                            new_kgm.save()
                            join_req.delete()
                            return Response(status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(status=status.HTTP_208_ALREADY_REPORTED)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)            


# creata a khatma within a khatma group where the sender is an admin of the khatma group
# add checking if the sender is an admin in the khatmagroup
class CreateKhatma(views.APIView):   
    permission_classes = [IsAuthenticated]
   
    def post(self,request,format=None): 
        
        seriliazer = khatmaSerializer(data=request.data)
        
        if seriliazer.is_valid():
            data = seriliazer.validated_data
            
            user = request.user
            try:
                khatmagroup = khatmaGroup.objects.get(name=data['G_name'])
                try:
                    khatma_G_Membership = khatmaGroupMembership.objects.get(user=user,role="admin",khatmaGroup=khatmagroup)
                    try:    
                        khatma = Khatma.objects.get(name=data["name"],period=data["period"],khatmaGroup=khatmagroup)
                    except:
                        khatma = None
                    if  khatma:
                        return Response(status=status.HTTP_208_ALREADY_REPORTED)
                    khatma = Khatma.objects.create(name=data["name"],period=data["period"],khatmaGroup=khatmagroup)
                    khatma.save()
                    try:
                        km = khatmaMembership.objects.create(khatma=khatma,khatmaGroupMembership=khatma_G_Membership)
                        km.save()
                        return  Response(status=status.HTTP_201_CREATED)
                    except:
                        return Response(data={"error": "but cannot create a khama membership"},status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(data={"error":"user not found"},status=status.HTTP_404_NOT_FOUND)
            except:
                return  Response(data={"error":"khatma group not found"},status=status.HTTP_404_NOT_FOUND)
        
        return Response(seriliazer.errors,status=status.HTTP_400_BAD_REQUEST)    
   
    def get(self,request,format=None): # list all user communties
        user = request.user
        query_set = khatmaGroupMembership.objects.filter(user=user)
        print(query_set)
        groups =[]
        for i in query_set:
            print(i.khatmaGroup)
            groups.append(i.khatmaGroup)
        print(groups)
        serializer = khatmaGroupSerializer(groups,many=True)
        print(serializer.data)
        # response = Response()
        # response["status"] = status.HTTP_200_OK
        # response['data']= serializer.data
        # response['datee']= "serializer.data"
        # return response
        return Response(serializer.data,status=status.HTTP_200_OK, content_type="application/json")
    
    
# add a member to a khatma (craete a user membership)
class khatma_memb(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = khatma_membSerializer(data = request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user
            
            try:
                khatmagroup = khatmaGroup.objects.get(name=data["G_name"])
                try:
                    khatma = Khatma.objects.get(name=data["KH_name"])
                    try:    
                        kgm = khatmaGroupMembership.objects.get(khatmaGroup=khatmagroup,user=user)
                    except:
                        return Response(data={"error":"member not Found"},status=status.HTTP_404_NOT_FOUND)
                except:
                    return Response(data={"error":"khatma not Found"},status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(data={"error":"khatmaGroup not Found"},status=status.HTTP_404_NOT_FOUND)
            try:
                km = khatmaMembership.objects.create(khatma=khatma,khatmaGroupMembership=kgm)
            except:
                return Response(status=status.HTTP_208_ALREADY_REPORTED)
            km.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

# list or retreive khatma
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

