from shortuuid import uuid
from rest_framework import status,views,serializers
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import api_view,permission_classes
from .models import group,groupMembership,groupSettings,groupCode
from .serializers import groupSerializer,groupDisplaySerializer,groupSettingsSerializer,groupCodeSerializer
from api.models import MyUser
from notification.tasks import push_added_to_group_notification
import logging


logger = logging.getLogger(__name__)



# create a group with one admin group membership which is the sender
class Group(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
   
    @extend_schema(
        request=groupSerializer,
        responses={
            201 :groupDisplaySerializer(),
            400: "Bad request, invalid data",
        },
        description="Create a new group with the authenticated user as the admin. Optionally, an icon can be uploaded for the group."
    )
    def post(self,request,format=None): # create a group with one admin group membership which is the sender
        serializer = groupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            data = serializer.validated_data
            gr = group.objects.create_group(name=data['name'],members=[user])
            
            if "icon" in data.keys():
                gr.icon.save(f'{data["name"]}',data['icon'])
                gr.save()
            data= groupDisplaySerializer(gr).data
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
    @extend_schema(
        responses={
            200: groupDisplaySerializer(many=True),
            403: "Forbidden, user not in group",
            404: "Group not found",
        },
        description="List all groups of the authenticated user."
    )
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
    
    @extend_schema(
        request=None,
        responses={
            204: "group deleted successfully",
            403: "Forbidden, only admin can delete a group",
            404: "Group not found",
        },
        description="Delete a group. Only the admin of the group can delete it."
    )
    def delete(self,request,*args,**kwargs): # delete a group by admin only
        user = request.user
        group_query = self.get_group_queryset()
        if not group_query:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
        group = group_query.first()
        is_admin = groupMembership.objects.filter(user=user,group=group,role="admin").exists()
        if not is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"Forbidden, only admin can delete a group"})
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
    
    @extend_schema(
        request=groupSettingsSerializer,
        responses={
            200: groupSettingsSerializer,
            403: "Forbidden, user not admin in group",
            404: "Group not found",
        },
        description="get group settings. Only the admin of the group can see the settings."
    )
    def get(self,request,*args,**kwargs): # get group settings 
        in_group = self.is_in_group() 
        if in_group == True:
            return self.retrieve(request,*args,**kwargs)
        elif in_group == "group not found":
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":in_group})
        elif in_group == "user not admin in group":
            return Response(status=status.HTTP_403_FORBIDDEN,data={"error":in_group})
    
    @extend_schema(
        request=groupSettingsSerializer,
        responses={
            200: groupSettingsSerializer,
            403: "Forbidden, user not admin in group",
            404: "Group not found",
        },
        description="Update group settings. Only the admin of the group can update the settings."
    )
    def post(self,request,*args,**kwargs): # update group settings
        
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
            

@extend_schema(
    parameters=[
        {
            "name": "group_id",
            "in": "path",
            "required": True,
            "description": "ID of the group to which the user will be added",
            "schema": {
                "type": "integer",
            },
        },
        {
            "username": "username",
            "in": "path",
            "required": True,
            "description": "Username of the user to be added to the group",
            "schema": {
                "type": "string",
            },
        },
    ],
    request=None,
    responses={
        201: "User added to group successfully",
        403: "Forbidden, not friends with the user",
        404: "Group or user not found",
    },
    description="Add a user to a group. The authenticated user must be friends with the user being added."
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_to_group(request,group_id): # add a member to a khatma
    user = request.user
    gr = group.objects.filter(id=group_id).first()
    # check group
    if not gr:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"group not found"})
    
    new_member  = MyUser.objects.filter(username=request.data['username']).first()
    # check new member
    if not new_member:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"member not found"})
    
    # check if the new member is in the list of the user's brothers
    if not new_member in user.brothers.all() and not new_member in user.brothers_set.all():
        return Response(status=status.HTTP_403_FORBIDDEN,data={"error":" not friends"})
    
    groupMembership.objects.create(group=gr,user=new_member,role="user")
    
    # push notification
    push_added_to_group_notification.delay(gr.name,gr.id,new_member.id,user.username)
    
    # log 
    logger.info(f"GROUP_JOIN: {new_member.username} joined {gr.name} : {gr.id} ")
    return Response(status=status.HTTP_201_CREATED,data={"msg":f"member added successfully to {gr.name}"})


@extend_schema(
    request=None,
    responses={
        204: "User exited group successfully",
        403: "Forbidden, user not in group",
        404: "Group not found",
    },
    description="Allows a user to exit a group. The user must be a member of the group to exit."
)
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
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


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
@extend_schema(
    request=None,
    responses={
        204: "User removed from group successfully",
        403: "Forbidden, user not admin in group",
        404: "Group or user not found",
    },
    description="Remove a user from a group. Only the admin of the group can remove a user."
)
def kick_user(request,group_id,user_id): # kick a user from a group
    user = request.user
    # check groupMembership 
    grMembership = groupMembership.objects.filter(user=user,group=group_id,role="admin").first()
    if not groupMembership:
        return Response(status=status.HTTP_403_FORBIDDEN,data={"error":"user not admin in group"})
    # check user to be kicked
    user_to_kick = MyUser.objects.filter(id=user_id).first()
    if not user_to_kick:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"user to be kicked not found"})
    # check user to be kicked in the group
    userGrMembership = groupMembership.objects.filter(user=user_to_kick,group=group_id).first()
    if not userGrMembership:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"user to be kicked not in group"})
    userGrMembership.delete()
    return Response(status=status.HTTP_204_NO_CONTENT,data={"msg":"user kicked successfully"})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "role": {
                    "type": "string",
                    "enum": ["admin", "user"],
                    "description": "New role for the user",
                }
            },
            "required": ["role"],
        }
    },
    responses={
        200: "User role changed successfully",
        400: "Bad request, invalid role",
        403: "Forbidden, user not admin in group",
        404: "Group or user not found",
    },
    description="Change the role of a user in a group. Only the admin of the group can change the role.",
)
def change_user_role(request,group_id,user_id):
    user = request.user
    # check group
    gr = group.objects.filter(id=group_id).first()
    if not gr:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "group not found"})
    
    # check if the user is admin in the group
    is_admin = groupMembership.objects.filter(user=user, role="admin", group=gr).exists()
    if not is_admin:
        return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "user not admin in group"})
    
    # check user to change role
    user_to_change = MyUser.objects.filter(id=user_id).first()
    if not user_to_change:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "user to change role not found"})
    
    # check user to change role in the group
    userGrMembership = groupMembership.objects.filter(user=user_to_change, group=gr).first()
    if not userGrMembership:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "user to change role not in group"})
    
    # change role
    new_role = request.data.get("role", None)
    if new_role not in ["admin", "user"]:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "invalid role"})
    
    userGrMembership.role = new_role
    userGrMembership.save()
    
    return Response(status=status.HTTP_200_OK, data={"msg": f"user role changed to {new_role} successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_group_code(request): # Generate a group code to add users via a link with a validation time
    
    serializer = groupCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    code = uuid()
    serializer.validated_data['code'] = code
    serializer.validated_data['issued_by'] = request.user
    try: 
        serializer.save()
    except serializers.ValidationError:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Group invitation code",
                }
            },
            "required": ["code"],
        }
    },
    responses={
        201: "User added to group successfully",
        404: "Code not found",
        410: "Code expired or deactivated",
        409: "User already in group",
    },
    description="Join a group using an invitation code. The code must be valid and not expired.",
)
def join_group_by_code(request):
    user = request.user
    code = request.data.get("code",None)
    # check for code
    if not code:
        return Response({"msg":"code not found"},status.HTTP_404_NOT_FOUND)
    
    gr_code = groupCode.objects.filter(code=code).first()
    
    if not gr_code:
        return Response({"msg":"code not found"},status.HTTP_404_NOT_FOUND)
    
    if not gr_code.is_valid():
        return Response({"msg":"code expired or deactivated"},status.HTTP_410_GONE)
    
    # check user in group
    if gr_code.group.membership.filter(user=user).exists():
        return Response({"msg":"user already in group"},status.HTTP_409_CONFLICT)
    
    # add user to group as a "user" role 
    gr_code.group.members.add(user)
    return Response({"msg":"user added to group successfully"},status.HTTP_201_CREATED)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Group invitation code to be deactivated",
                }
            },
            "required": ["code"],
        }
    },
    responses={
        200: "Code deactivated successfully",
        403: "Forbidden, user not authorized to deactivate the code",
        404: "Code not found",
        409: "Code already deactivated",
    },
    description="Deactivate a group invitation code. Only the user who issued the code or an admin of the group can deactivate it.",
)
def deactivate_group_code(request):
    user = request.user
    code = request.data.get("code",None)
    
    if not code:
        return Response({"msg":"code not found"},status.HTTP_404_NOT_FOUND)
    
    gr_code = groupCode.objects.filter(code=code).first()
    
    if not gr_code:
        return Response({"msg":"code not found"},status.HTTP_404_NOT_FOUND)

    if not gr_code.issued_by == user and not gr_code.group.membership.filter(user=user,role="admin").exists():
        return Response({"msg":"forbidden"},status.HTTP_403_FORBIDDEN)
    
    if not gr_code.is_valid():
        return Response({"msg":"code already inactive or expired"},status.HTTP_409_CONFLICT)
    
    gr_code.active = False
    gr_code.save()
    
    return Response({"msg":"code deactivated successfully"},status.HTTP_200_OK)
    

class code(ListModelMixin):
    pass