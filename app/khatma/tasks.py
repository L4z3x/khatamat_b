from celery import shared_task
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message,Notification 
import logging

logger = logging.getLogger(__name__)

@shared_task
def push_added_to_group_notification(group_name,group_id,user_id,adder_name):
    device = FCMDevice.objects.filter(user_id=user_id).first()
    
    message = Message(
        notification=Notification(
            title=f'Welcome to {group_name}',
            body=f'You have been added to a {group_name} by {adder_name}'
        ),
        data={'group_id': str(group_id)}
    )
    if device:
        device.send_message(message)
    else:
        # Handle the case where the device does not exist with a redirect or something else
        # log this event or take other actions   
        logger.error(f"Device not found for user {device.user.username} with id {device.user.id}")

