from rest_framework import generics,views
from .models import MyUser,brothership
from rest_framework import status 
from .serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated,AllowAny

@extend_schema(operation_id="get_user_list")
class ListUserapi(generics.ListAPIView,generics.RetrieveAPIView): # remove in production
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

@extend_schema(operation_id="create_user_account")
class CreateUserapi(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        return self.create(request)

@extend_schema(operation_id="delete_user_account")
class DeleteUserapi(generics.DestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def delete(self,request,id = None):
        if id:
            user = MyUser.object.get(id=id)
            if request.user == user:
                return self.destroy(request,id)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error":"id doesn't match the sender's"})
        else:
            return Response('No id specified',status=status. HTTP_400_BAD_REQUEST)

@extend_schema(
    operation_id="get_user_brother_list",
    summary="get brother list"
)
class brother(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,**args): # get brothers
        user = request.user
        id = self.kwargs.get('id')
        print(id)
        if id:
            brother = MyUser.objects.filter(id=id).first()
            
            # add private to user model default is False
            if brother.private == True and user not in brother.brothers.all() and user not in brother.brothers_set.all():
                return Response(data={"msg":"private accounte"},status=status.HTTP_302_FOUND) 

            brothers = brother.brothers.all().union(brother.brothers_set.all())
        else:
            brothers = user.brothers.all().union(user.brothers_set.all())

        serializer = brotherDataSer(brothers,many=True).data

        if serializer:
            return Response(serializer,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
    

@extend_schema(responses=brotherDataSer,operation_id="update_user")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user

    serializer = UserSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        print(serializer.validated_data)    

    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)
    
    serializer.save()
    
   
    return Response(status=status.HTTP_202_ACCEPTED,data={"msg":"updated succesfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@extend_schema(operation_id="delete_brother")
def deleteBrother(request,id): # remove a brother from your list
    user = request.user
    try:
        brother = MyUser.objects.get(id=id)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":f"{e}"})
    br = brothership.objects.filter(user1=user,user2=brother) | brothership.objects.filter(user1=brother,user2=user) 
    if not br.exists():
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"you are not brothers yet"})
    br = br.first()
    br.delete()
    return Response(status=status.HTTP_200_OK,data={"msg":f"{brother.username} removed"})


@extend_schema(responses=brotherDataSer,operation_id="get_mutual_brothers")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mutualBrother(request, id): # get mutual brother of a brother
    user = request.user
    try:
        brother = MyUser.objects.get(id=id)
    except MyUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Brother not found"})
    
    user_brothers = set(user.brothers.all())
    brother_brothers = set(brother.brothers.all())
    mutual_brothers = user_brothers.intersection(brother_brothers)
    
    mutual_brothers.discard(brother)
    mutual_brothers.discard(user)
    if not mutual_brothers:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"msg": "No mutual brothers"})
    
    serializer = brotherDataSer(mutual_brothers, many=True).data
    return Response(status=status.HTTP_200_OK, data=serializer)

@extend_schema(responses=brotherDataSer,operation_id="get_blocked_list")
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

@api_view(['POST'])
@extend_schema(operation_id="block_brother")
@permission_classes([IsAuthenticated])
def blockBrother(request,id): # block a brother
    user = request.user

    try:
        blocked = MyUser.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"msg":"no id associated with that Id"})

    # check for friends to delete
    if user.brothers.filter(id=blocked.id).exists():
        user.brothers.remove(blocked)
    # check for friends to delete
    if user.brothers_set.filter(id=blocked.id).exists():
        user.brothers_set.remove(blocked)

    user.blocked.add(blocked)
    user.save()
    
    return Response(status=status.HTTP_202_ACCEPTED)
