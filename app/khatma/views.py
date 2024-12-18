from group.models import group
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from khatma.models import Khatma,khatmaMembership,groupMembership,group
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from drf_spectacular.utils import extend_schema
from .serializers import khatma_membSerializer,khatmaSerializer,khatmaDisplaySerializer
    
    
class khatma_membership(RetrieveUpdateDestroyAPIView,CreateModelMixin,ListModelMixin):# add a member to a khatma (create a user membership)
    """
    API view to handle khatma membership operations including retrieval, update, deletion, and creation.
    
    Methods
    -------
    get_queryset():
        Returns the queryset of all khatma memberships.
    get_khatmaMembeship_queryset():
        Returns the queryset for a specific khatma membership based on the provided ID.
    patch(request, *args, **kwargs):
        Updates a khatma membership for the authenticated user. The user must be a member of the group associated with the khatma.
    post(request, *args, **kwargs):
        Creates a new khatma membership for the authenticated user. The user must be a member of the group associated with the khatma.
    get(request, *args, **kwargs):
        Retrieves khatma share status by khatma membership ID or lists all khatma memberships of members in a khatma.
    list_all_for_group(request, *args, **kwargs):
        Lists khatma memberships of all members in a khatma for the khatma info page.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = khatma_membSerializer
    lookup_field = 'id'
    queryset = khatmaMembership.objects.all() # TODO: check the N+1 problem ansijami for performence

    def get_khatmaMembeship_queryset(self):    
        try:
            id = self.kwargs['id']
        except:
            id = None
        if id == None:
            return khatmaMembership.objects.none()
        return khatmaMembership.objects.filter(id=id)
     
    @extend_schema(
        request=khatma_membSerializer,
        responses={
            201: khatma_membSerializer,
            400: "Bad request, invalid data",
            403: "Forbidden, user not in group",
            404: "Khatma or group not found",
        },
        operation_id="update_khatma_membership",
        description="update khatma membership for the authenticated user. The user must be a member of the group associated with the khatma."
    )
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
    
    @extend_schema(
        request=khatma_membSerializer,
        responses={
            201: khatma_membSerializer,
            400: "Bad request, invalid data",
            403: "Forbidden, user not in group",
            404: "Khatma or group not found",
        },
        operation_id="create_khatma_membership",
        description="Create a new khatma membership for the authenticated user. The user must be a member of the group associated with the khatma."
    )  
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
    
    @extend_schema(
        request=khatma_membSerializer,
        responses={
            200: khatma_membSerializer,
            403: "Forbidden, user not in group",
            404: "Khatma membership not found",
        },
        operation_id="retrieve_khatma_membership",
        summary="Retrieve Khatma Membership",
        description="Retrieve the khatma membership details by khatma membership ID.",
    )
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
    
    @extend_schema(
        request=khatma_membSerializer,
        responses={
            200: khatma_membSerializer,
            403: "Forbidden, user not in group",
            404: "Khatma membership not found",
        },
        operation_id="list_all_khatma_memberships",
        summary="List All Khatma Memberships",
        description="List all khatma memberships of members in a khatma for the khatma info page.",
    )
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
@extend_schema(
    request=None,
    responses={
        200: khatma_membSerializer(many=True),
        403: "Forbidden, user not authenticated",
    },
    operation_id="list_khatmas_of_user",
    summary="List Khatmas of User",
    description="Retrieve all khatma memberships for the authenticated user.",
)
def list_khatmas_of_user(request): # display all khatma memberships of a user
        user = request.user
        kh = khatmaMembership.objects.filter(user=user).all()
        data = []
        for membership in kh:
            serializer = {}
            serializer['progress'] = membership.progress
            serializer['group'] = membership.khatma.group.name 
            serializer['group_id'] = membership.khatma.group.pk
            serializer['endDate'] = membership.khatma.endDate
            serializer['khatma'] = membership.khatma.name
            serializer['khatma_id'] = membership.khatma.pk
            serializer['status'] = membership.status
            data.append(serializer)
        
        return Response(status=status.HTTP_200_OK,data={"data":data})

# create update retrieve delete khatma
class khatma_details(RetrieveUpdateDestroyAPIView,CreateModelMixin):
    """
    A APIView that provides retrieve, update, destroy, and create actions for Khatma objects.
    Methods:
        get_queryset:
            Returns the queryset of all Khatma objects.
        get_khatma_queryset:
            Returns the queryset of a specific Khatma object based on the 'id' in the URL.
        post:
            Creates a new Khatma object. Checks if the user has permission to create a Khatma in the specified group.
        put:
            Updates an existing Khatma object within the update timeout range. Checks if the user is an admin or the launcher of the Khatma.
        get:
            Retrieves the details of a specific Khatma object based on the 'id' in the URL. Checks if the user is a member of the group.
        delete:
            Deletes a Khatma object within the delete timeout range. Checks if the user is an admin or the launcher of the Khatma.
    """
    
    serializer_class = khatmaSerializer
    permission_class = [IsAuthenticated]
    
    UPDATE_TIMEOUT = timedelta(minutes=15) 
    DELETE_TIMEOUT = timedelta(minutes=15) 
    queryset = Khatma.objects.all()
    lookup_field = 'id'
    def get_khatma_queryset(self):
        try:
            id = self.request.params.get['id']
        except:
            id = None
        if id == None:
            return Khatma.objects.none()
        return Khatma.objects.filter(id=id) 

    @extend_schema(
        request=khatmaSerializer,
        responses={
            200: khatmaSerializer,
            403: "Forbidden, user is not admin or launcher in the group",
            404: "Khatma not found",
            406: "Not Acceptable, update timeout exceeded",
        },
        operation_id="update_khatma",
        summary="Update Khatma",
        description="Update a khatma's information within the update timeout range. The user must be an admin or the launcher of the khatma.",
    )
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

    
    @extend_schema(
        request=khatmaSerializer,
        responses={
            200: khatmaSerializer,
            403: "Forbidden, user is not in the group",
            404: "Khatma not found",
        },
        operation_id="retrieve_khatma_details",
        summary="Retrieve Khatma Details",
        description="Retrieve the details of a specific Khatma object based on the 'id' in the URL. The user must be a member of the group associated with the Khatma.",
    )
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
    


    @extend_schema(
        request=None,
        responses={
            204: "Khatma deleted successfully",
            403: "Forbidden, user is not admin or launcher in the group",
            404: "Khatma not found",
            406: "Not Acceptable, delete timeout exceeded",
        },
        operation_id="delete_khatma",
        summary="Delete Khatma",
        description="Delete a Khatma object within the delete timeout range. it will work if the timeout exceeded and there was no khatma membership, and thThe user must be an admin or the launcher of the Khatma.",
    )
    def delete(self,request,*args,**kwargs): # delete a khatma (by admin or launcher in the first 15 min)        
        user = request.user
        
        queryset = self.get_queryset()
        if not queryset.exists(): # check khatma existance
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        khatma = queryset.first()
        group = khatma.group
        
        is_admin = groupMembership.objects.filter(group=group,user=user,role="admin").exists()
        is_launcher = khatma.launcher == user
        khatma_members_exists = khatma.khatmamembership_set.all().count() > 1
        if khatma.created_at + self.DELETE_TIMEOUT > timezone.now() and khatma_members_exists:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if is_launcher or is_admin: # remember to add code for pushing notification
            return self.destroy(request,*args,**kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            

class create_khatma(APIView,CreateModelMixin):
    permission_class = [IsAuthenticated]
    queryset = Khatma.objects.all()
    def get_serializer(self,*args,**kwargs):
        return khatmaSerializer(*args,**kwargs)
    
    
    @extend_schema(
        request=khatmaSerializer,
        responses={
            201: khatmaSerializer,
            208: "Already Reported, khatma with this name already exists in this group",
            400: "Bad request, invalid data",
            403: "Forbidden, user is not admin in group",
        },
        operation_id="create_khatma",
        summary="Create Khatma",
        description="Create a new khatma for the authenticated user. The user must be a member of the group associated with the khatma. If the group settings do not allow all members to launch khatmas, the user must be an admin.",
    )
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
                except:                    
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"error":"user is not admin in group"},status=status.HTTP_400_BAD_REQUEST)
       
        else:
            # check if it's a member in the khatma group
            is_member = groupMembership.objects.filter(user=user,group=gr).exists()
            if is_member:
                try:
                    return self.create(request,*args,**kwargs)
                except Exception as e:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data={"error":f"could not create khatma{e}"}) 
            return Response(data={"error":"user not found in group"},status=status.HTTP_400_BAD_REQUEST)
    
        
# create update
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@extend_schema(
    request=None,
    responses={
        200: khatmaDisplaySerializer(many=True),
        403: "Forbidden, user not in group",
        404: "Group not found",
    },
    operation_id="list_khatmas_of_group",
    summary="List Khatmas of Group",
    description="Retrieve all khatmas of a specific group. The user must be a member of the group to view the khatmas.",
)
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

