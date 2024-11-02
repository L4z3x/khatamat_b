from rest_framework import generics,views
from .models import MyUser,brothership
from rest_framework import status 
from .serializers import *
from rest_framework.decorators import api_view,permission_classes
from notification.serializers import brothershipSerializer
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


class brother(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request): # get brothers
        user = request.user
        if request.GET.get('id'):
            brother = MyUser.objects.get(id=request.GET.get('id'))
            if user.private == True: # add private to user model default is False
                if not user in brother.brothers:
                    return Response(data={"msg":"private accounte"},status=status.HTTP_302_FOUND)
            brothers = brother.brothers.all() | brother.brothers_set.all() 
        else:
            brothers = user.brothers.all() | user.brothers_set.all()
        print(brothers)
        serializer = brotherDataSer(brothers,many=True).data
        print(serializer)
        if serializer:
            return Response(serializer,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    def post(self,request,format=None):
        user = request.user
        pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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


def blockBrother(request): # block a brother
    pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mutualBrother(request,id): #get mutual friends if account is not private
    user = request.user
    try:
        brother = MyUser.objects.get(id=id)
    except Exception as e: # remove in production
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":f"{e}"}) 
    
    br_brother_1 = brother.brothership_initiated.all()
    br_brother_2 = brother.brothership_received.all()
    br_user_1 = user.brothership_initiated.all()
    br_user_2 = user.brothership_received.all()
    match = []
    # matching algorithm 
    for br1 in br_brother_1:
        for br2 in br_user_1:
            if br2.user2 == br1.user2 and br2.user2 != brother and br1.user2 != user:
                match.append(br1.user2)
        for br2 in br_user_2:
            if br2.user1 == br1.user2 and br2.user1 != brother and br1.user2 != user:
                match.append(br1.user2)
    for br1 in br_brother_2:
        for br2 in br_user_1:
            if br2.user2 == br1.user1 and br2.user2 != brother and br1.user1 != user:
                match.append(br1.user1)
        for br2 in br_user_2:
            if br2.user1 == br1.user1 and br2.user1 != brother and br1.user1 != user:
                match.append(br1.user1)
    if not match:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"msg":"no mutual brothers"})    
    serializer = brotherDataSer(match,many=True).data
    return Response(status=status.HTTP_200_OK,data=serializer)

    # print(brBr)
    # print(brBr2)
    # print(br_brother)
    # print(br_user)
    # for br1 in br_brother:
        # for br2 in br_user:
            # if br2.user1 == br1.user1 or br2.user1 == br1.user2
 