from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from api.models import MyUser,brothership
from notification.models import joinRequest,brothershipRequest
from rest_framework import views,status
from rest_framework.decorators import api_view,permission_classes
from khatma.models import khatmaGroup
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import RetrieveAPIView 




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
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_brothershipReq(request):
    serializer = brothershipSerializer(data=request.data)
    user = request.user
    if serializer.is_valid() and user:
        data = serializer.validated_data
        id = data.get('id')
        try:
            brother = MyUser.objects.get(id=id)
            if brother == user:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE,data={"error":"user connot be brother with himself !!!"})
            try:
                br = brothershipRequest.objects.create(owner=user,brother=brother,status='pending')
                br.save()
            except Exception as e:
                return Response(status=status.HTTP_208_ALREADY_REPORTED,data={f"error":f"{e}"})
        except:
            return Response(data={"error":"this user doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        return Response(data={"msg":f"brothership Request sent to {brother.username}"},status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_brothershipReq(request):
    user = request.user
    serializer = brothershipSerializer(data= request.data)
    if serializer.is_valid() and user:
        data = serializer.validated_data
        id = data.get('id')
        requester = MyUser.objects.get(id=id) # add whatever you want to send from the client side
        try:
            br =  brothershipRequest.objects.get(owner= requester,brother=user,status="pending") # check for the brothership request
        except:
            return Response(data={"error":"brothershipRequest not found"},status= status.HTTP_404_NOT_FOUND)
        if br:
            if not brothership.objects.get(user1=requester,user2=user).exist():
                new_brothership = brothership.objects.create(user1=requester,user2=user) # create a new brothership
                new_brothership.save()
                br.status = "accepted"
                br.save()
            else:
                return Response(status=status.HTTP_302_FOUND)
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_brothershipReq(request):
    user = MyUser.objects.get(username=request.user)
    print(user)
    try:
        req = brothershipRequest.objects.filter(owner=user) | brothershipRequest.objects.filter(brother=user)
        sen_data= []        
        rec_data = []
        for r in req:
            receiver = r.owner
            serializer = brothershipReqDataSer(receiver).data
            serializer['since']= r.created_at
            if receiver == user:
                sen_data.append(serializer)
            else:
                rec_data.append(serializer)
        print(sen_data)
        print(rec_data)
        req2 = user.incoming_brothership_req.all()
        print(req2)
       
    except Exception as e:
        return Response(data={"error":f"{e}"},status=status.HTTP_404_NOT_FOUND)
    print(req)
        
    try:
        serializer = brothershipReqSerialiazer(req,many=True)
        
    except:
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(data={"recieved":rec_data,"sent":sen_data},status=status.HTTP_200_OK)
    


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_brothership(request):
#     user = request.user
#     if request.GET.get('id'):
#         user = MyUser.objects.get(id=id)
#     else :
#         user = request.user        
    
#     print(id)
#     print(user.username)
#     return Response(status=status.HTTP_400_BAD_REQUEST)