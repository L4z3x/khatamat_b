# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import group, message,groupMembership
from .serializer import messageSerializer
from channels.db import  database_sync_to_async

@database_sync_to_async
def get_group_Mem(group,user): # return group Membership by user and group
    return groupMembership.objects.filter(group=group,user=user).first()

@database_sync_to_async
def get_group(id): # return group by id
    return group.objects.filter(id=id).first()

@database_sync_to_async
def create_message(group,userMem,text): # creates a message by group and membership and text 
    msg = message.objects.create(group=group,sender=userMem,message=text)
    data = messageSerializer(msg).data
    return data

@database_sync_to_async
def update_message(group,userMem,text,id): # update a message by group and membership and text
    msg = message.objects.get(group=group,sender=userMem,id=id)
    msg.message = text
    msg.save()
    data = messageSerializer(msg).data
    return data

@database_sync_to_async
def get_message(id,user):
    return message.objects.filter(id=id,user=user)

@database_sync_to_async
def deleteMessage(id,group_id,user_id=None):
    msg = message.objects.filter(id=id,group=group_id,sender=user_id).first()
    if msg == None:
        return "cannot find message"
    try:
        msg.message = ''
        msg.removed = True
    except:
        return "cannot delete message"
    return "message deleted succesfully"


class groupConsumer(AsyncWebsocketConsumer):
    async def connect(self): # connect user and him to group channel layer
        self.user = self.scope['user']
        # check if user is authenticated . just when using the query string jwt middleware
        # to be removed in production 
        if self.user.is_authenticated == False:
            await self.close()    

        await self.accept()
        
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"chat_{self.group_id}" 
        
        # check group id
        self.group = await get_group(self.group_id)
        if not self.group:
            return await self.disconnect(code='your not in that group')

        # check user membership in that group
        self.group_mem = await get_group_Mem(self.group,self.user)
        if not self.group_mem:
            return await self.disconnect(code='your not in that group')
        
        await self.channel_layer.group_add(self.group_name,self.channel_name)
          
    async def receive(self ,text_data=None, bytes_data=None): # receive incomming websockets
        
        data = json.loads(text_data)
        action = data["action"]
        
        if action == 'send_message':
            await self.send_message(data['msg'])
        elif action == 'update_message':
            await self.update_message(data['msg'],data['msg_id'])
        elif action == 'delete_message':
            await self.delete_message(data['msg_id'])
        elif action == 'delete_message_as_admin':
            await self.delete_message_as_admin(data['msg_id'])
        else:
            await self.send(text_data="undefined action")
        
    async def send_group_message(self,type,id,text=None,time=None,error=None): # send to all group channels
        
        await self.channel_layer.group_send(self.group_name,{
            "type": type,
            "message":
                {
                    "text": text,
                    "time": time,
                    "group": self.group_id,
                    "id":id,
                    "error": error,
                    
                }
            })
    
    async def chat_message(self,event): # send data to each channel in the group layer:
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def send_message(self,text): # send message to group 
        msg = await create_message(self.group,self.group_mem,text)
        if not msg['message']:
            return await self.send(text_data="error bad request")
        await  self.send_group_message(text=msg['message'],type="chat_message",id=msg['id'],time=msg['created_at'])
  
    async def delete_message(self,id): # delete a message in a group
        msg = await deleteMessage(id,self.user)
        if msg == "cannot find message":
            return await self.send(text_data=msg)
        elif msg == "cannot delete message":
            return await self.send(text_data=msg)
        return await self.send_group_message(type="chat_message",id=id)
        
    async def delete_message_as_admin(self,id):
        if not self.group_mem.role == "admin":
            return await self.send(text_data="you're not admin of this group")
        msg = await deleteMessage(id)
        if msg == "cannot find message":
            return await self.send(text_data=msg)
        elif msg == "cannot delete message":
            return await self.send(text_data=msg) # TODO: to be checked
        return await self.send_group_message(id=id,type="chat_message")
        
    async def update_message(self,text,id):
        msg = await update_message(self.group,self.group_mem,text,id)
        await self.send_group_message(msg['message'],type="chat_message",id=msg['id'],time=msg['created_at'])
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        await self.send(text_data=json.dumps({
            "type":"disconnected",
            "code":code,
            }))
        await self.close()

class twoPchatConsumer(AsyncWebsocketConsumer): # private chat consumer
    async def connect(self):
        self.user = self.scope['user']
        # check if user is authenticated . just when using the query string jwt middleware
        # to be removed in production 
        if self.user.is_authenticated == False:
            await self.close()    
        
        await self.accept()
    
    
    async def receive(self, text_data=None, bytes_data=None):
        return await super().receive(text_data, bytes_data)