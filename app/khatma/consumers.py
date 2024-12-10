# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import group, message,groupMembership,media
from .serializer import messageSerializer
from api.models import MyUser
from channels.db import  database_sync_to_async
from json.decoder import JSONDecodeError


@database_sync_to_async
def get_group_Mem(group,user): # return group Membership by user and group
    return groupMembership.objects.filter(group=group,user=user).first()


@database_sync_to_async
def get_group(id): # return group by id
    return group.objects.filter(id=id).first()


@database_sync_to_async
def create_message(group,userMem,text,timestamp,reply_to=None): # creates a message by group and membership and text 
    
    if reply_to:
        reply_to = group.messages.filter(id=reply_to).first()
        if not reply_to:
            return "msg not found"
        if reply_to.removed == True:
            return "msg deleted"
        
    msg = message.objects.create(group=group,
                                 sender=userMem,
                                 message=text,
                                 reply=reply_to,
                                 created_at=timestamp)
    
    data = messageSerializer(msg).data
    return data


@database_sync_to_async
def send_message_notifications(msg):
    """
    push notification to user with celery
    """
    pass


@database_sync_to_async
def update_message(userMem,text,id,user_id,timestamp): # update a message by group and membership and text
    user = MyUser.objects.filter(id=user_id).first()
    if not user:
        return "not found"
    # ensure the sender is the owner of the message
    sender_mem = user.groupMembership.filter(id=userMem.id).first()
    msg = sender_mem.sentMessages.filter(id=id).first()
    if not msg:
        return "not found"
    msg.message = text
    msg.updated_at = timestamp
    msg.save()
    data = messageSerializer(msg).data
    return data


@database_sync_to_async
def deleteMessage(id,user_mem,group):
    if user_mem.role == "admin":
        msg = message.objects.filter(group=group,id=id).first()
    else:
        msg = user_mem.sentMessages.filter(id=id).first()
    
    if msg == None:
        return "cannot find message"
    try:
        msg.message = ''
        msg.removed = True
        """
        handle deleting a file if it exists
        """
        if msg.file != None:
            msg.file.file.delete() # delete the file associated wit the instance
            msg.file.save()
            msg.file = None
            msg.file# delete the media instance
        msg.save()
    except Exception as e:
        return f"{e} cannot delete message"
    return "message deleted succesfully"


class groupConsumer(AsyncWebsocketConsumer):
    
    async def connect(self): # connect user to group channel layer
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
        
        return await self.channel_layer.group_add(self.group_name,self.channel_name)
          

    async def receive(self ,text_data=None, bytes_data=None): # receive incomming websockets
        try:
            data = json.loads(text_data)
        except JSONDecodeError:
            return await self.send(text_data="json error") # malformed json data error 
        except:
            return await self.send(text_data="error")
        action = data.get("action",None)
        reply = data.get('reply', None)
        msg = data.get('msg',None)
        msg_id = data.get("msg_id",None)
        timestamp = data.get("timestamp",None)
        match action:
            case 'send_message':
                return await self.send_message(text=msg,timestamp=timestamp,reply=reply)
            case 'update_message':
                return await self.update_message(text=msg,id=msg_id,timestamp=timestamp)
            case 'delete_message':
                return await self.delete_message(msg_id)
            case 'delete_message_as_admin':
                return await self.delete_message_as_admin(msg_id)
            case 'disconnect':
                return await self.disconnect(code=1000)
            case _:
                return await self.send(text_data="undefined action")
        

    async def send_group_message(self,type,id,action, file=None, text=None, time=None,reply=None): # send to all group channels
        
        await self.channel_layer.group_send(self.group_name,{
            "type": type,
            "message":
                {
                    "action": action,
                    "text": text,
                    "time": time,
                    "group": self.group_id,
                    "id":id,
                    "file":file,
                    "reply": reply,
                    
                }
            })

    
    async def chat_message(self,event): # send data to each channel in the group layer:
        message = event['message']
        await self.send(text_data=json.dumps(message))


    async def send_message(self,text,timestamp,reply=None,url=None): # send message to group     
        if not timestamp:
            return await self.send(text_data="missing timestamp filed")
        if not text:
            return await self.send(text_data="missing text filed")
        msg = await create_message(self.group,self.group_mem,
                                   text=text,
                                   reply_to=reply,
                                   timestamp=timestamp, # need to be checked
                                   )
        
        if msg == "msg not found" or msg == "msg deleted" or "URI not valid:" in msg :
            return await self.send(text_data=msg)
        if not msg['message']:
            return await self.send(text_data="error bad request")
        await  self.send_group_message(text=msg['message'],
                                       type="chat.message",
                                       id=msg['id'],
                                       action="send_message",
                                       time=msg['created_at'],
                                       reply=msg.get("reply",None)
                                       )

  
    async def delete_message(self,id): # delete a message in a group
        msg = await deleteMessage(id,self.group_mem,group=self.group)

        if msg == "cannot find message" or "cannot delete message" in msg:
            return await self.send(text_data=msg)

        return await self.send_group_message(type="chat.message",
                                             action="send_message",
                                             id=id)

        
    async def delete_message_as_admin(self,id):    
        if not self.group_mem.role == "admin":
            return await self.send(text_data="you're not admin of this group")
        msg = await deleteMessage(id,self.group_mem,group=self.group)

        if msg == "cannot find message" or msg == "cannot delete message":
            return await self.send(text_data=msg)

        return await self.send_group_message(id=id,
                                             type="chat.message",
                                             action= "delete_message_as_admin"
                                             )


    async def update_message(self,text,id,timestamp):
        msg = await update_message(userMem=self.group_mem,
                                   text=text,
                                   id=id,
                                   user_id=self.user.id,
                                   timestamp=timestamp)
        
        if msg == "not found" or msg == "not allowed":
            return await self.send(text_data=msg)
        
        return await self.send_group_message(text=msg['message'],
                                             type="chat.message",
                                             action="send_message",
                                             id=msg['id'],
                                             time=msg['updated_at'],
                                             reply=msg.get('reply',None)
                                             )
             
                                      
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