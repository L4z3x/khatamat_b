from khatma.serializer import *
from api.models import MyUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from khatma.models import Khatma,khatmaMembership,groupMembership,group
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.decorators import api_view,permission_classes
from drf_spectacular.utils import extend_schema
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import mimetypes

# create a group with one admin group membership which is the sender

class Group(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self,request,format=None): # create a group with one admin group membership which is the sender
        serializer = groupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            data = serializer.validated_data
            gr = group.objects.create_group(name=data['name'],members=[user])
            
            if "icon" in data.keys():
                gr.icon.save(f'{data['name']}',data['icon']) # search about media folder and some stuff abt image field
                gr.save()
                
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def get(self,request): # list all groups of a user
        user = request.user
        query_set = groupMembership.objects.filter(user=user)
        groups =[]

        for i in query_set:
            groups.append(i.group)

        serializer = groupDisplaySerializer(groups,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def get_group_queryset(self):
        try:
            id = self.request.data["group_id"]
        except:
            id = None
        if id:
            return group.objects.filter(id=id)
        return group.objects.none()
    
    def delete(self,request,*args,**kwargs): # delete a khatma group by admin only
        user = request.user
        group_query = self.get_group_queryset()
        if not group_query:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
        group = group_query.first()
        is_admin = groupMembership.objects.filter(user=user,group=group,role="admin").exists()
        if not is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"only admin can delete a group"})
        try:
            group.delete()
        except:
            return Response(status=status.http40)
        return Response(status=status.HTTP_204_NO_CONTENT,data={"msg":"group deleted successfully"})
    
# manage group settings 
class group_settings(RetrieveUpdateAPIView,ListModelMixin):
    serializer_class = groupSettingsSerializer 
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        try:
            id = self.kwargs['id']
        except:
            id = None
        if not id:
            return groupSettings.objects.none()
        return groupSettings.objects.filter(group=id)
    
    def is_in_group(self):
        user = self.request.user
        settings_queryset = self.get_queryset()
        if not settings_queryset:
            return "group not found"
        settings = settings_queryset.first()
        gr = settings.group

        is_admin = gr.membership.filter(user=user,role="admin",group=gr).exists()

        if not is_admin:
            return "user not admin in group"
        return True
    
    def get(self,request,*args,**kwargs): # get group settings 
        in_group = self.is_in_group() 
        if in_group == True:
            return self.retrieve(request,*args,**kwargs)
        elif in_group == "group not found":
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":in_group})
        elif in_group == "user not admin in group":
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":in_group})
    
    def post(self,request,*args,**kwargs):
        
        in_group = self.is_in_group()
        if in_group == "group not found":
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":in_group})
        elif in_group == "user not in group":
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":in_group})
        elif in_group == True: 
            is_admin = groupMembership.objects.filter(user=request.user,role="admin").exists()
            if not is_admin:
                return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user not admin in the group"})
            return self.partial_update(request,*args,**kwargs)
            
# add a member to a khatma
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_to_group(request,group_id):
    user = request.user
    gr = group.objects.filter(id=group_id).first()
    # check group
    if not gr:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
    
    new_member  = MyUser.objects.filter(id=request.data['user_id']).first()
    # check new member
    if not new_member:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"member not found"})
    
    # check if the new member is in the list of the user's brothers
    if not new_member in user.brothers.all() and not new_member in user.brothers_set.all():
        return Response(status=status.HTTP_403_FORBIDDEN,data={"error":" not friends"})
    
    groupMembership.objects.create(group=gr,user=new_member,role="user")
    return Response(status=status.HTTP_201_CREATED,data={"msg":f"member added successfully to {gr.name}"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def exit_group(request,group_id): # user exiting a group
    user = request.user
    gr = group.objects.filter(id=group_id).first()
    
    # check group
    if not gr:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
    # check user in group
    if not gr in user.group.all():
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"user not in group"})
    
    userMembership = groupMembership.objects.filter(user=user,group=gr).first()
    userMembership.delete()
    return Response(status=status.HTTP_204_NO_CONTENT,data={"msg":"user removed from khatma successfully"})
    
    
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
     
    def patch(self, request, *args, **kwargs): # update a khatma membership like share and progress
        user = request.user
        queryset = self.get_khatmaMembeship_queryset()
        khatma_Membership =  queryset.first()
        print(khatma_Membership)
        if not queryset.exists():
            if not khatma_Membership.groupMembership.user == user:
                return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"no khatma membership found for the user"})
        self.queryset = queryset
        data = self.partial_update(request,*args,**kwargs)
        khatma_Membership.khatma.save()
        return Response(status=status.HTTP_202_ACCEPTED,data={"data":data.data})
        
    def post(self,request,*args,**kwargs): # join a khatma and take your share
        user = request.user
        # create share 
        if not Khatma.objects.filter(id=request.data['khatma']).exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"no khatma with that id"})
        
        khatma = Khatma.objects.filter(id=request.data['khatma']).first()
        group = khatma.group
        if not groupMembership.objects.filter(user=user,group=group).exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"user not member in the group yet"})
        return self.create(request,*args,**kwargs)
        
    def get(self,request,*args,**kwargs): # retrieve khatma share status   by khatma membership id (???) 
        user = request.user
        try: 
            id = self.kwargs['id']
        except:
            id = None
            
        if id == None:
            # retrieve all khatma memberships of members in a khatma 
            return self.list_all_for_group(request,*args,**kwargs)
            
        # retrieving one single khatma membership
        queryset = self.get_khatmaMembeship_queryset()
        
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"khatma membership not found"})

        # checking user membership in the group
        if not queryset.first().groupMembership.group in user.group.all():
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user not member in the group"})
        
        self.queryset = queryset
        return self.retrieve(request,*args,**kwargs)
    
    def list_all_for_group(self,request,*args,**kwargs): # list khatma memberships of all members in that khatma for khatma info page
        user = request.user
        gr = group.objects.filter(id=request.query_params.get('g', None)).first()
            # check group existance
        if not gr:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
            
        # check user membership in the group
        if not gr in user.group.all():
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user is not in the group"})
            
        khatma = Khatma.objects.filter(id=request.query_params.get('kh', None)).first()
            
        if not khatma:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        self.queryset = khatmaMembership.objects.filter(khatma=khatma).all()
        return self.list(request,*args,**kwargs)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_khatmas_of_user(request): # display all khatma memberships of a user
        user = request.user
        kh = khatmaMembership.objects.filter(user=user,status='ongoing').all()
        print(kh)
        data = []
        for membership in kh:
            serializer = {}
            serializer['progress'] = membership.progress
            serializer['group'] = membership.khatma.group.name 
            serializer['group_id'] = membership.khatma.group.pk
            serializer['endData'] = membership.khatma.endDate
            serializer['khatma'] = membership.khatma.name
            data.append(serializer)
        
        return Response(status=status.HTTP_200_OK,data={"data":data})

# create update retrieve delete khatma
class khatma_details(RetrieveUpdateDestroyAPIView,CreateModelMixin):
    serializer_class = khatmaSerializer
    permission_class = [IsAuthenticated]
    lookup_field  = 'id'
    
    UPDATE_TIMEOUT = timedelta(minutes=15) 
    DELETE_TIMEOUT = timedelta(minutes=15) 
    
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
        gr = group.objects.filter(id=data['group']).first()

        
        
        if Khatma.objects.filter(group=gr,name=data['name']).exists():
            return Response(status=status.HTTP_208_ALREADY_REPORTED,data={"error":"khatma with this name already exists in this group"})
        # check if the group give the permission to users to launch khatmas
        if gr.settings.All_can_launch_khatma == False:
            # check if the user is admin in the group
            is_admin = groupMembership.objects.filter(user=user,role="admin",group=gr).exists()
            if is_admin:        
                try:
                    return self.create(request,*args,**kwargs)
                except Exception as e:
                    print(e)
                    
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"error":"user is not admin in group"},status=status.HTTP_400_BAD_REQUEST)
       
        else:
            # check if it's a member in the khatma group
            is_member = groupMembership.objects.filter(user=user,group=gr).exists()
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
        is_admin_in_group = groupMembership.objects.filter(user=user,role="admin", group=khatma.group).exists()
        
        is_launcher_in_group = khatma.launcher == user
        
        if not is_admin_in_group and not is_launcher_in_group:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "User is not admin or launcher in the group."})
        
        return self.partial_update(request,*args,**kwargs)

    def get(self,request,*args,**kwargs): # get one khatma details by id in the url
        queryset = self.get_khatma_queryset()
        
        # Check if Khatma exists
        if not queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Khatma not found."})
        
        khatma = queryset.first()
        
        # Check if the user is in the group
        user = request.user
        user_in_group = groupMembership.objects.filter(
            user=user, group=khatma.group
        ).exists()
        
        if not user_in_group:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "User is not in the group."})
        return self.retrieve(request,*args,**kwargs)
        
    def delete(self,request,*args,**kwargs): # delete a khatma (by admin or launcher in the first 15 min)        
        user = request.user
        
        queryset = self.get_queryset()
        if not queryset.exists(): # check khatma existance
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        khatma = queryset.first()
        group = khatma.group
        
        is_admin = groupMembership.objects.filter(group=group,user=user,role="admin").exists()
        is_launcher = khatma.launcher == user
        
        if khatma.created_at + self.DELETE_TIMEOUT > timezone.now():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if is_launcher or is_admin: # remember to add code for pushing notification
            return self.destroy(request,*args,**kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
            
# create update
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_khatmas_of_group(request,group_id): # get khatmas of a group 
    user = request.user
    gr= group.objects.filter(id=group_id).first()
    if not gr:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
    if not user in gr.members.all():
        return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user not in group"})
    khatmas = gr.khatma_set.all()
    print(khatmas)
    current = []
    history = []
    for khatma in khatmas:
        if khatma.endDate < timezone.now():
            history.append(khatma)
            user
        else:
            current.append(khatma)

    current = khatmaDisplaySerializer(current,many=True).data
    history = khatmaDisplaySerializer(history,many=True).data

    return Response(status=status.HTTP_200_OK,data={"current":current,"history":history})

    
class messagePagination(CursorPagination):    
    ordering = "-created_at" 

    
class list_messages(ListAPIView):
    serializer_class = messageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = messagePagination
    
    def get_queryset(self):
        msg_id = self.request.query_params.get('msg_id', None)
        if msg_id != None:
            msg = message.objects.filter(id=msg_id,group=self.kwargs['group_id'],removed=False).first()
            if not msg:
                return message.objects.none()    
            return message.objects.filter(group=self.kwargs['group_id'],created_at__gte = msg.created_at) # .order_by("-created_at")
        return message.objects.filter(group=self.kwargs['group_id']) # .order_by("-created_at")
    """
    fetches 10 recent created msgs by default
    if a msg_id is specified then fetched msgs starting from that msg
    """
    def get(self,request,*args,**kwargs):
        user = request.user
        group_id = self.kwargs['group_id']
        
        # check user membership in the group 
        is_in_group = groupMembership.objects.filter(group=group_id,user=user).exists()
        if not is_in_group:
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user not in group"})
        return self.list(request,*args,**kwargs)


def validated_file_size(file):
    max_size = 50 * 1024 * 1024  # 50 MB
    if file.size > max_size:
        return False
    return True


supported_mime_types = [
    # Images
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml', 'image/bmp', 'image/tiff',
    
    # Videos
    'video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/webm',
    
    # Audio
    'audio/mpeg', 'audio/ogg', 'audio/wav', 'audio/webm', 'audio/aac', 'audio/mp4', 'audio/x-wav', 'audio/flac',
    
    # Documents
    'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'text/plain',
    
    # Archives
    'application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed', 'application/gzip',
]


def validated_file_type(file):
    mime_type, encoding = mimetypes.guess_type(file.name)
    if mime_type not in supported_mime_types:
        return False
    return True

    
class FileUploadMessage(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    lookup_field = 'group_id'
    
    def post(self, request, *args, **kwargs):
        # Extract file and group information
        file = request.FILES['file']
        group_id = self.kwargs['group_id']
        if not validated_file_size(file):
            return Response("file too large",status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if not validated_file_type(file):
            return Response("unsupported media type",status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        msg = request.data.get("msg",None)
        reply = request.data.get("reply",None)
        user_mem = request.user.groupMembership.filter(group=group_id).first()
        
        if reply:
            reply = message.objects.filter(id=reply).first() # get the instance
            if not reply:
                return Response("message not found",status=status.HTTP_404_NOT_FOUND)
        
        gr = group.objects.filter(id=group_id).first()
        if not gr:
            return Response("group not found",status=status.HTTP_404_NOT_FOUND)
        
        # Save the file in the Media model
        file = media.objects.create(
            file=file
        )
        msg = message.objects.create(
            group= gr,
            sender= user_mem,
            message= msg,
            reply= reply,
            file=file,
            file_path= file.file.url
        )
        file_type, encoding = mimetypes.guess_type(file.file.path) # get the file type
        # Generate file metadata
        metadata = {
            "id": file.id,
            "url": file.file.url,
            "file_name": file.file.name,
            "file_type": file_type,
            "file_size": file.file.size,
        }

        # Broadcast file metadata via WebSocket
        channel_layer = get_channel_layer()
        group_name = f"chat_{gr.id}"  # Channel Layer group name for the chat
        msg_data = messageSerializer(msg).data
        message_data = {
                    "action": "send_message",
                    "text": msg_data["message"],
                    "time": msg_data["created_at"],
                    "group": msg_data["group"],
                    "id": msg_data['id'] ,
                    "file":metadata,
                    "reply": msg_data["reply"],
                }
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "chat_message",
                "message": message_data,
            },
        )
        return Response(status.HTTP_201_CREATED)

        # Return the file metadata as HTTP response    
    