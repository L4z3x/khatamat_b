from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from api.models import MyUser,brothership
from notification.models import joinRequest,brothershipRequest
from rest_framework import views,status
from rest_framework.decorators import api_view,permission_classes
from khatma.models import khatmaGroup,khatmaGroupMembership
from rest_framework.response import Response
from .serializers import *
from api.serializers import brotherDataSer
from drf_spectacular.utils import extend_schema




# tested and working >>> send multiple join requests to admins of a khatma group
class create_JoinRequest(views.APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'group_name'
    
    def post(self,request,group_name,format=None): # to be updated more to handle more errors.
        if group_name and len(group_name) < 50:
            user = request.user
            try:
                khatmagroup = khatmaGroup.objects.get(name=group_name)
            except:
                return Response(data={"error":"khatma group not found"},status=status.HTTP_404_NOT_FOUND)
            adminsMem = khatmagroup.khatma_G_membership.filter(role="admin")
            print(adminsMem)
            senders = adminsMem.values_list("user",flat=True)
            print(senders)
            admins =[]
            for i in senders:
                print(i)
                try:
                    sender = MyUser.objects.get(id=i)
                    join_req = joinRequest.objects.get(sender=sender,receiver=user,khatmaGroup=khatmagroup)
                except:
                    join_req = None
                if not join_req:
                    joinrequest = joinRequest.objects.create(sender=sender,receiver=user,khatmaGroup=khatmagroup)
                    joinrequest.save()
                    admins.append(joinrequest.sender.username)
                if not admins:
                    return Response(data={"msg":"requset already sent"},status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    print(admins)
                    return Response(data={"msg":"request sent","admins number":f"{len(admins)}"},status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_brothershipReq(request,id):
    sender = request.user
    if id:
        try:
            receiver = MyUser.objects.get(id=id)
            if receiver == sender: # just for fun ;)
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE,data={"error":"user connot be brother with himself !!!"})
            # check if they are brothers already
            if brothership.objects.filter(user1=sender,user2=receiver).exists() or brothership.objects.filter(user1=receiver,user2=sender).exists():
                return Response(data={"error":"you are already brothers"},status=status.HTTP_302_FOUND)
            try:
                br = brothershipRequest.objects.create(sender=sender,receiver=receiver,status='pending')
                br.save()
            except Exception as e:
                return Response(status=status.HTTP_208_ALREADY_REPORTED,data={f"error":f"{e}"})
        except:
            return Response(data={"error":"this user doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        return Response(data={"msg":f"brothership Request sent to {receiver.username}"},status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_brothershipReq(request,id):
    user = request.user
    if id:
        sender = MyUser.objects.get(id=id) # add whatever you want to send from the client side
        print(sender.pk)
        try:
            br =  brothershipRequest.objects.get(sender=sender,receiver=user) # check for the brothership request
            print(br)
        except Exception as e:
            return Response(data={"error":f"brothershipRequest not found ###{e}"},status= status.HTTP_404_NOT_FOUND)
        if br:
            if brothership.objects.filter(user1=sender,user2=user).exists() or brothership.objects.filter(user1=user,user2=sender).exists():
                return Response(data={"error":"you are already brothers"},status=status.HTTP_302_FOUND)
            
            new_brothership = brothership.objects.create(user1=sender,user2=user) # create a new brothership
            new_brothership.save()
            br.status = "accepted"
            br.save()
            return Response(data={"msg":f"{sender.username} accepted"},status=status.HTTP_201_CREATED)
        return Response(data={"error":f"brothershipRequest not found"},status= status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST,data={"error":"no id was passed with the url"})


@extend_schema(responses=brotherDataSer)
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # /* add status to brothership request serialiazer and view *
def list_brothershipReq(request):
    user = request.user
    try:
        req = brothershipRequest.objects.filter(sender=user,status='pending') | brothershipRequest.objects.filter(receiver=user,status='pending')
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
    except Exception as e:
        return Response(data={"error":f"{e}"},status=status.HTTP_404_NOT_FOUND)
    return Response(data={"recieved":rec_data,"sent":sen_data},status=status.HTTP_200_OK)
    
@api_view(['POST'])
@extend_schema(
    operation_id="deny_brothership_request",
    responses={200: 'Success'}
)
@permission_classes([IsAuthenticated])
def deny_brothershipReq(request,id):
    user = request.user
    try:
        br = brothershipRequest.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"no brothership request with associated with that id"})
    if br.receiver == user:
        br.status = 'rejected'
        br.save()
        return Response(status=status.HTTP_202_ACCEPTED,data={"msg":"the brothership req was rejected succesfully"})
    else:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,data={"msg":"the request was not meant for you"})

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
    try:
        sender = MyUser.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"id of sender not found"})

    # check khatma group existance
    try:
        kh_group = khatmaGroup.objects.get(name=name)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"khatma group not found"})

    # check if user is admin of that khatma group 
    if not khatmaGroupMembership.objects.filter(user=user,khatmaGroup=kh_group,role="admin").exists():    
        return Response(status=status.HTTP_401_UNAUTHORIZED,data={"error":"your not admin of this khatma group"})

    try:
        join_req = joinRequest.objects.get(sender=sender,receiver=user,status="pending")
    except:
        if joinRequest.objects.filter(sender=sender,receiver=user,status="accepted").exists():
            return Response(status=status.HTTP_302_FOUND,data={"msg":"join request already accepted"})
        return Response(status=status.HTTP_404_NOT_FOUND,data={"error":"join request not found"})
    
    join_req.status = "accepted"
    join_req.save()
    
    new_kh_g_Membership = khatmaGroupMembership.objects.create(user=sender,role="user",khatmaGroup=kh_group)
    new_kh_g_Membership.save()

    return Response(status=status.HTTP_202_ACCEPTED,data={"msg":f"accepted join request from {sender.username} to {kh_group.name}"})

