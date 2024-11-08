# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import khatmaGroup, message,khatmaGroupMembership
from .serializer import messageSerializer
from channels.db import  database_sync_to_async

@database_sync_to_async
def get_group_Mem(group,user):
    return khatmaGroupMembership.objects.get(khatmaGroup=group,user=user)

@database_sync_to_async
def get_group(id):
    return khatmaGroup.objects.get(id=id)

@database_sync_to_async
def create_message(group,userMem,text):
    msg = message.objects.create(group=group,sender=userMem,message=text)
    data = messageSerializer(msg).data
    return data


@database_sync_to_async
def update_message(group,userMem,text,id):
    msg = message.objects.get(group=group,sender=userMem,id=id)
    msg.message = text
    msg.save()
    data = messageSerializer(msg).data
    return data


class khatmaGroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        # check if user is authenticated .
        if self.user.is_authenticated == False:
            await self.close()    

        await self.accept()
        
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"chat_{self.group_id}" 
        
        # check khatma id
        try:
            self.group = await  get_group(self.group_id)
        except:
            return await self.disconnect(code='no khatma group with such id')
        
        # check user membership in that khatma group
        try:
            self.group_mem = await get_group_Mem(self.group,self.user)
        except:
            await self.disconnect(code='your not in that khatma group')
        
        await self.channel_layer.group_add(self.group_name,self.channel_name)
    
        
    async def receive(self ,text_data=None, bytes_data=None):
        
        text = json.loads(text_data)
        action = text["action"]
        
        if action == 'send_message':
            await self.send_message(text['msg'])
        elif action == 'update_message':
            await self.update_message(text['msg'],text['id'])
        elif action == 'delete_message':
            await self.delete_message(text['msg'])
        elif action == 'delete_message_as_admin':
            await self.delete_message_as_admin(text['msg'])
        
    async def send_group_message(self,text,type,time,id,group,error=None):
        
        await self.channel_layer.group_send(self.group_name,{
            "type": type,
            "message":
                {
                    "text": text,
                    "time": time,
                    "group": group,
                    "id":id,
                    "error": error,
                    
                }
            })
    
    # send data to each channel in the group:
    async def chat_message(self,event):
        print(event)
        message = event['message']
        await self.send(text_data=json.dumps(message))


    async def send_message(self,text):
        msg = await create_message(self.group,self.group_mem,text)
        print(msg)
        if not msg['message']:
            await self.send_group_message("error bad request",type="error",id=None,time=None)
        await  self.send_group_message(msg['message'],group=self.group.name,type="chat_message",id=msg['id'],time=msg['created_at'])
    
    
    async def update_message(self,text,id):
        msg = await update_message(self.group,self.group_mem,text,id)
        await self.send_group_message(msg['message'],group=self.group.name,type="chat_message",id=msg['id'],time=msg['updated_at'])
        
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

