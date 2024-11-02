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


def deleteBro(request): # remove a brother from your list
    pass

def blockBro(request): # block a brother
    pass

def mutualBro(request): #get mutual friends if account is not private
    pass    
