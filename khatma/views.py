from khatma.serializer import *
from api.models import MyUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from khatma.models import Khatma,khatmaMembership,khatmaGroupMembership,khatmaGroup
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.decorators import api_view,permission_classes
from drf_spectacular.utils import extend_schema


# create a khatmaGroup with one admin group membership which is the sender
@extend_schema(
    
)
class Group(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self,request,format=None): # create a khatmaGroup with one admin group membership which is the sender
        serializer = khatmaGroupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            data = serializer.validated_data
            khatma_group = khatmaGroup.objects.create_khatmaGroup(name=data['name'],members=[user])
            
            if "icon" in data.keys():
                khatma_group.icon.save(f'{data['name']}',data['icon']) # search about media folder and some stuff abt image field
                khatma_group.save()
                
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def get(self,request): # list all groups of a user
        user = request.user
        query_set = khatmaGroupMembership.objects.filter(user=user)
        groups =[]

        for i in query_set:
            groups.append(i.khatmaGroup)

        serializer = khatmaGroupSerializer(groups,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


# add a member to a khatma
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_to_group(request,id):
    user = request.user
    group = khatmaGroup.objects.filter(id=id).first()
    # check group
    if not group:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
    
    new_member  = MyUser.objects.filter(id=request.data['user_id']).first()
    # check new member
    if not new_member:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"member not found"})
    
    # check if the new member is in the list of the user's brothers
    if not new_member in user.brothers.all() and new_member in user.brothers_set.all():
        return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user and member are not friends"})
    
    khatmaGroupMembership.objects.create(khatmaGroup=group,user=new_member,role="user")
    return Response(status=status.HTTP_201_CREATED,data={"msg":f"member added successfully to {group.name}"})
    
    
# add a member to a khatma (create a user membership)
class khatma_membership(RetrieveUpdateDestroyAPIView,CreateModelMixin,ListModelMixin):
    
    permission_classes = [IsAuthenticated]
    serializer_class = khatma_membSerializer
    lookup_field = 'id'
    
    def get_queryset(self): # TODO: check the N+1 problem ansijami for performence
        return khatmaMembership.objects.all() 
    
    def get_khatmaMembeship_queryset(self):    
        try:
            id = self.kwargs['id']
        except:
            id = None
        if id == None:
            return khatmaMembership.objects.none()
        return khatmaMembership.objects.filter(id=id)
     
    def patch(self, request, *args, **kwargs):
        # update khamta membership
        user = request.user
        queryset = self.get_khatmaMembeship_queryset()
        khatma_Membership =  queryset.first()
        if queryset.exists():
            if khatma_Membership.khatmaGroupMembership.user == user:
                self.queryset = queryset
                return self.partial_update(request,*args,**kwargs)
        
    def post(self,request,*args,**kwargs): # join a khatma and take your share
        user = request.user
        # create share 
        if not Khatma.objects.filter(id=request.data['khatma']).exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"no khatma with that id"})
        
        khatma = Khatma.objects.filter(id=request.data['khatma']).first()
        group = khatma.khatmaGroup
        if not khatmaGroupMembership.objects.filter(user=user,khatmaGroup=group).exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"user not member in the group yet"})
        return self.create(request,*args,**kwargs)
        
    def get(self,request,*args,**kwargs): # list khatma share status
        user = request.user
        try: 
            id = self.kwargs['id']
        except:
            id = None
            
        if id == None:
            # retrieve all khatma memberships
            return self.list_all(request,*args,**kwargs)
            
        # retrieving one single khatma membership
        queryset = self.get_khatmaMembeship_queryset()
        
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"khatma membership not found"})

        # checking user membership in the group
        if not queryset.first().khatmaGroupMembership.khatmaGroup in user.khatmaGroup.all():
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user not member in the group"})
        
        self.queryset = queryset
        return self.retrieve(request,*args,**kwargs)
    
    def list_all(self,request,*args,**kwargs):
        user = request.user
        group = khatmaGroup.objects.filter(id=request.query_params.get('g', None)).first()
            # check group existance
        if not group:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
            
        # check user membership in the group
        if not group in user.khatmaGroup.all():
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user is not in the group"})
            
        khatma = Khatma.objects.filter(id=request.query_params.get('kh', None)).first()
            
        if not khatma:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        self.queryset = khatmaMembership.objects.filter(khatma=khatma).all()
        print(self.queryset)
        print(self.filter_queryset(self.get_queryset()))
        return self.list(request,*args,**kwargs)
    

# create update retrieve delete khatma
class khatma_details(RetrieveUpdateDestroyAPIView,CreateModelMixin):
    serializer_class = khatmaSerializer
    permission_class = [IsAuthenticated]
    lookup_field  = 'id'
    
    UPDATE_TIMEOUT = timedelta(minutes=15) 
    DELETE_TIMEOUT = timedelta(minutes=15) 
    
    def get_khatmagroup(id):
        return khatmaGroup.objects.filter(id=id).first()
    
    def get_queryset(self): # get khatma query set
        return Khatma.objects.all()
    
    def get_khatma_queryset(self):
        try:
            id = self.kwargs['id']
        except:
            id = None
        if id == None:
            return Khatma.objects.none()
        return Khatma.objects.filter(id=id) 
    
    def post(self,request,*args,**kwargs): # launch a khatma 
        user = request.user
        data = request.data
        khatmagroup = self.get_khatmagroup(data['khatmaGroup'])
        if Khatma.objects.filter(khatmaGroup=khatmagroup,name=data['name']).exists():
            return Response(status=status.HTTP_208_ALREADY_REPORTED,data={"error":"khatma with this name already exists in this group"})
        # check if the group give the permission to users to launch khatmas
        if khatmagroup.settings.All_can_launch_khatma == False:
            # check if the user is admin in the group
            is_admin = khatmaGroupMembership.objects.filter(user=user,role="admin",khatmaGroup=khatmagroup).exists()
            if is_admin:        
                try:
                    return self.create(request,*args,**kwargs)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"error":"user is not admin in group"},status=status.HTTP_400_BAD_REQUEST)
       
        else:
            # check if it's a member in the khatma group
            is_member = khatmaGroupMembership.objects.filter(user=user,khatmaGroup=khatmagroup).exists()
            if is_member:
                try:
                    return self.create(request,*args,**kwargs)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST) 
            return Response(data={"error":"user not found in group"},status=status.HTTP_400_BAD_REQUEST)
       
    def put(self,request,*args,**kwargs): # update a khatma info within the the update_timeout range
        queryset = self.get_khatma_queryset()
        
        # Check if Khatma exists
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Khatma not found."})
        
        khatma = queryset.first()
        
        # Check if the user is in the group
        user = request.user
        
        if khatma.created_at + self.DELETE_TIMEOUT > timezone.now():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        is_admin_in_khatmagroup = khatmaGroupMembership.objects.filter(user=user,role="admin", khatmaGroup=khatma.khatmaGroup).exists()
        
        is_launcher_in_khatmagroup = khatma.launcher == user
        
        if not is_admin_in_khatmagroup or not is_launcher_in_khatmagroup:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "User is not admin or launcherin the group."})
        
        return self.partial_update(request,*args,**kwargs)

    def get(self,request,*args,**kwargs): # get one khatma details by id in the url
        queryset = self.get_khatma_queryset()
        
        # Check if Khatma exists
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Khatma not found."})
        
        khatma = queryset.first()
        
        # Check if the user is in the group
        user = request.user
        user_in_khatmagroup = khatmaGroupMembership.objects.filter(
            user=user, khatmaGroup=khatma.khatmaGroup
        ).exists()
        
        if not user_in_khatmagroup:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "User is not in the group."})
        return self.retrieve(request,*args,**kwargs)
        
    def delete(self,request,*args,**kwargs): # delete a khatma (by admin or launcher in the first 15 min)        
        user = request.user
        
        queryset = self.get_queryset()
        if not queryset.exists(): # check khatma existance
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        khatma = queryset.first()
        khatmagroup = khatma.khatmaGroup
        
        is_admin = khatmaGroupMembership.objects.filter(khatmaGroup=khatmagroup,user=user,role="admin").exists()
        is_launcher = khatma.launcher == user
        
        if khatma.created_at + self.DELETE_TIMEOUT > timezone.now():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if is_launcher or is_admin: # remember to add code for pushing notification
            return self.destroy(request,*args,**kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
            
# add view to list all khatma of a group in specific way [current,history] (allow pagination)