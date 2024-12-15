from celery import shared_task
from fcm_django.models import FCMDevice 
from firebase_admin.messaging import Message,Notification 
from logging import getLogger

logger = getLogger(__name__)

@shared_task
def push_message_notification(users_id, message, group_name,link=None,conversation=None,reply=None):
    """
    Push notification to users using Celery.
    Note: This task must only contain synchronous code since Celery does not support async tasks.
    """
    notification = Notification(title=group_name, body=message)
    data = {
        "group": group_name,
        "link": str(link) if link else "",
        "type": "message",
        "reply": str(reply) if reply else "",
        "conversation": str(conversation) if conversation else "",
    }

    for user_id in users_id:
        device = FCMDevice.objects.filter(user=user_id).first()
        if device:
            device.send_message(Message(notification=notification, data=data))
        else:
            logger.error(f"Device not found for user with ID {user_id}")

@shared_task
def push_req_notification(user_id,message,title,time,link=None):
    """
    push request notification  
    """
    type = "friendship_request"
    device = FCMDevice.objects.filter(user=user_id).first()
    message = Message(notification=Notification(title=title,body=message),
                        data={  "link":str(link),
                                "type":type,
                                "time":time
                            })
    if device:
        device.send_message(message)
    else:
        # Handle the case where the device does not exist with a redirect or something else
        # log this event or take other actions   
        logger.error(f"Device not found for user {device.user.username} with id {device.user.id}")
