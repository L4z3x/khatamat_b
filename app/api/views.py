from rest_framework import generics,views
from rest_framework.generics import RetrieveUpdateAPIView
from .models import MyUser,brothership
from rest_framework import status 
from .serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import OpenApiResponse
# add extend_schema with details so the developers will understand everything with operation id, summary, description, and responses

# ----------------- user -----------------

@extend_schema(
    operation_id="user_setting",
    summary="Retrieve or update user settings",
    description="This endpoint allows authenticated users to retrieve or update their settings. "
                "GET request retrieves the settings, while PUT request updates the settings.",
    responses={
        200: UserSettingSerializer,
        404: OpenApiResponse(description="No settings found"),
        400: OpenApiResponse(description="Bad request")
    }
)
class User_Setting(RetrieveUpdateAPIView):
    serializer_class = UserSettingSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserSetting.objects.all()
    lookup_field = 'user_id'
    
    def get(self,request,*args,**kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        if not self.queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"no settings found"})
        return self.retrieve(request,*args,**kwargs)   
    
    def put(self,request,*args,**kwargs):
        user = request.user
        self.queryset = self.queryset.filter(user=user)
        if not self.queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"no settings found"})
        return self.partial_update(request,*args,**kwargs)
            

@extend_schema(
    operation_id="delete_user_account",
    summary="Delete a user account",
    description="This endpoint allows authenticated users to delete their account. "
                "The user must provide their ID, and the ID must match the authenticated user's ID.",
    responses={
        204: OpenApiResponse(description="User deleted successfully"),
        400: OpenApiResponse(description="Bad request, ID doesn't match the sender's or no ID specified"),
        404: OpenApiResponse(description="User not found")
    }
)
class DeleteUser(generics.DestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def delete(self,request,id = None):
        if id: # additional check (token + id)
            user = MyUser.object.get(id=id)
            if request.user == user: 
                return self.destroy(request,id)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error":"id doesn't match the sender's"})
        else:
            return Response('No id specified',status=status. HTTP_400_BAD_REQUEST)


# ----------------- brothership -----------------

@extend_schema(
    operation_id="list_friends",
    summary="Retrieve a list of friends",
    description="This endpoint allows authenticated users to retrieve a list of their friends. "
                "The response includes a list of friends associated with the authenticated user.",
    responses={
        200: brotherDataSer,
        404: OpenApiResponse(description="No brothers found")
    }
)
class brother(views.APIView): # get brothers
    permission_classes = [IsAuthenticated]
    
    def get(self,request,**args): # get brothers
        user = request.user
        
        brothers = user.brothers.all().union(user.brothers_set.all())

        serializer = brotherDataSer(brothers,many=True).data

        if serializer:
            return Response(serializer,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
@extend_schema(
    operation_id="delete_brother",
    summary="Delete a brother from the user's list",
    description="allows authenticated users to remove a brother from their list. "
                "The user must provide the brother's ID. If the brother is found and the relationship exists, "
                "it will be deleted.",
    responses={
        200: OpenApiResponse(description="Brother removed successfully"),
        404: OpenApiResponse(description="Brother not found or not in the user's list"),
        400: OpenApiResponse(description="Bad request")
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteBrother(request,id): # remove a brother from your list
    user = request.user
    
    brother = MyUser.objects.filter(id=id).first()
    
    if not brother:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"brother not found"})
    
    br = brothership.objects.filter(user1=user,user2=brother) | brothership.objects.filter(user1=brother,user2=user) 
    
    if not br.exists():
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"you are not brothers"})
    
    br = br.first()
    br.delete()
    
    return Response(status=status.HTTP_200_OK,data={"msg":f"{brother.username} removed"})


@extend_schema(
    operation_id="list_mutual_user",
    summary="Retrieve mutual users",
    description="This endpoint allows authenticated users to retrieve a list of mutual friends they share with another user. "
                "The user must provide the user's ID. The response includes a list of mutual friends.",
    responses={
        200: brotherDataSer,
        404: OpenApiResponse(description="user not found"),
        400: OpenApiResponse(description="Bad request")
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mutualBrother(request, id): # get mutual brother of a brother
    user = request.user
    
    brother = MyUser.objects.filter(id=id).first()
    if not brother:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Brother not found"})
    
    user_brothers = set(user.brothers.all())
    brother_brothers = set(brother.brothers.all())
    
    mutual_brothers = user_brothers.intersection(brother_brothers)
    
    mutual_brothers.discard(brother)
    mutual_brothers.discard(user)
    
    if not mutual_brothers:
        return Response(status=status.HTTP_200_OK, data={})
    
    serializer = brotherDataSer(mutual_brothers, many=True).data
    return Response(status=status.HTTP_200_OK, data=serializer)


# ----------------- block -----------------

@extend_schema(
    operation_id="list_blocked",
    summary="Retrieve blocked users",
    description="This endpoint allows authenticated users to retrieve a list of users they have blocked. "
                "The response includes a list of blocked users.",
    responses={
        200: brotherDataSer(many=True),
        400: OpenApiResponse(description="Bad request")
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_blocked(request):
    user = request.user
    blocked = user.blocked.all()
    if not blocked:
        return Response(status=status.HTTP_200_OK,data={})
    data = []
    for block in blocked:
        serializer = brotherDataSer(block).data
        data.append(serializer)
    return Response(status=status.HTTP_200_OK,data=data)

@extend_schema(
    operation_id="block_user",
    summary="Block a User",
    description="This endpoint allows authenticated users to block a User. "
                "The user must provide the user's ID. If the brother is found, they will be blocked.",
    responses={
        200: OpenApiResponse(description="User blocked successfully"),
        404: OpenApiResponse(description="User not found"),
        400: OpenApiResponse(description="Bad request")
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blockBrother(request,id): # block a brother
    user = request.user

    
    blocked = MyUser.objects.filter(id=id).first()
    if not blocked:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"msg":"no id associated with that Id"})

    # check for brothers to delete
    if user.brothers.filter(id=blocked.id).exists():
        user.brothers.remove(blocked)
    # check for brothers to delete
    if user.brothers_set.filter(id=blocked.id).exists():
        user.brothers_set.remove(blocked)

    user.blocked.add(blocked)
    user.save()
    
    return Response(status=status.HTTP_202_ACCEPTED)
