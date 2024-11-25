from rest_framework.permissions import IsAuthenticated
from api.models import MyUser,brothership
from notification.models import joinRequest,brothershipRequest
from rest_framework import views,status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import *
from api.serializers import brotherDataSer
from drf_spectacular.utils import extend_schema
from community.models import communityMembership



# if authentication of commuity is not none, send multiple join requests to admins of a community 
class create_JoinRequest(views.APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'community_id'
    
    def post(self,request,group_name,format=None): # to be updated more to handle more errors.
        user = request.user
            
        commu = community.objects.filter(name=group_name).first()

        if not commu:
            return Response(data={"error":"community not found"},status=status.HTTP_404_NOT_FOUND)
        if commu.authentication == "none":
            commu.members.add(user)
            return Response(status=status.HTTP_202_ACCEPTED,data={"msg":f"added to {commu.name}"})
        adminsMem = commu.membership.filter(role="admin").all()
        admins =[]
        for admin in adminsMem:
            join_req = joinRequest.objects.filter(sender=user,receiver=admin.user,community=commu)

            if not join_req:
                joinrequest = joinRequest.objects.create(sender=user,receiver=admin.user,community=commu)
                joinrequest.save()
                admins.append(joinrequest.receiver.username)
        if not admins:
            return Response(data={"msg":"requset already sent"},status=status.HTTP_208_ALREADY_REPORTED)
        else:
            return Response(data={"msg":"request sent","admins number":f"{len(admins)}"},status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_brothershipReq(request,id):
    sender = request.user
    receiver = MyUser.objects.filter(id=id).first()
            
    if receiver == sender: # just for fun ;)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,data={"error":"user connot be brother with himself !!!"})
            
        # check if they are brothers already
    if brothership.objects.filter(user1=sender,user2=receiver).exists() or brothership.objects.filter(user1=receiver,user2=sender).exists():
        return Response(data={"error":"you are already brothers"},status=status.HTTP_302_FOUND)
            
    br = brothershipRequest.objects.create(sender=sender,receiver=receiver,status='pending')
    br.save()
    return Response(data={"msg":f"brothership Request sent to {receiver.username}"},status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_brothershipReq(request,user_id):
    user = request.user
    
    sender = MyUser.objects.filter(id=user_id).first()# add whatever you want to send from the client side
    if not sender:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"user not found"})
    
    if brothership.objects.filter(user1=sender,user2=user).exists() or brothership.objects.filter(user1=user,user2=sender).exists():
        return Response(data={"error":"you are already brothers"},status=status.HTTP_302_FOUND)

    br =  brothershipRequest.objects.filter(sender=sender,receiver=user).first() # check for the brothership request            return Response(data={"error":f"brothershipRequest not found ###{e}"},status= status.HTTP_404_NOT_FOUND)
    if not br:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"brothershiprequest not found"})
        
    br.status = "accepted"
    br.save()
            
    new_brothership = brothership.objects.create(user1=sender,user2=user) # create a new brothership
    new_brothership.save()
    return Response(data={"msg":f"{sender.username} accepted"},status=status.HTTP_201_CREATED)


@extend_schema(responses=brotherDataSer)
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # /* add status to brothership request serialiazer and view *
def list_brothershipReq(request):
    user = request.user
    
    req = brothershipRequest.objects.filter(sender=user,status='pending') | brothershipRequest.objects.filter(receiver=user,status='pending')
    if not req:
        return Response(data={"error":"no request found"},status=status.HTTP_404_NOT_FOUND)

    sen_data= []        
    rec_data = []
    for r in req:
        receiver = r.sender
        serializer = brotherDataSer(receiver).data
        serializer['since']= r.created_at
        serializer['id'] = r.pk
        if receiver == user:
            sen_data.append(serializer)
        else:
            rec_data.append(serializer)
    return Response(data={"recieved":rec_data,"sent":sen_data},status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deny_brothershipReq(request,id):
    user = request.user
    br = brothershipRequest.objects.filter(id=id).first()
    if not br:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"no brothership request with associated with that id"})
    if br.receiver == user:
        br.status = 'rejected'
        br.save()
        return Response(status=status.HTTP_202_ACCEPTED,data={"msg":"the brothership req was rejected succesfully"})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,data={"msg":"the request was not meant for you"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_joinReq(request,id):
    user = request.user
    
    serializer = joinRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)
    else:
        name = serializer.validated_data['g_name']

    # check sender
    sender = MyUser.objects.filter(id=id).first()
    if not sender:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"id of sender not found"})

    # check khatma group existance
    commu = community.objects.get(name=name)
    if not commu:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"commu not found"})

    # check if user is admin of that khatma group 
    if not community.membership.objects.filter(user=user,group=commu,role="admin").exists():    
        return Response(status=status.HTTP_401_UNAUTHORIZED,data={"error":"your not admin of this community"})

    if joinRequest.objects.filter(sender=sender,receiver=user,status="accepted").exists():
        return Response(status=status.HTTP_302_FOUND,data={"msg":"join request already accepted"})
    
    join_req = joinRequest.objects.filter(sender=sender,receiver=user,status="pending",community=commu).first()
    if not join_req:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"join request not found"})
    join_req.status = "accepted"
    join_req.save()
    
    new_commu_Membership = communityMembership.objects.create(user=sender,role="user",community=commu)
    new_commu_Membership.save()

    return Response(status=status.HTTP_202_ACCEPTED,data={"msg":f"accepted join request from {sender.username} to {commu.name}"})

